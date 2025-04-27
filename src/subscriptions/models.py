import helpers.billing
from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save
from django.conf import settings
from django.urls import reverse
from django.db.models import Q

User = settings.AUTH_USER_MODEL
ALLOW_CUSTOM_GROUPS = True

SUBSCRIPTION_PERMISSIONS = [
            ('advanced', 'Advanced Perm'),
            ('pro', 'Pro Perm'),
            ('basic', 'Basic Perm'),
            ('basic ai', 'Basic AI Perm'),
        ]

class Subscription(models.Model):
    '''
    Stripe Product - Subscription Model to manage subscription plan and permissions.
    '''
    name = models.CharField(max_length=120)
    subtitle = models.TextField(blank=True, null=True)
    groups = models.ManyToManyField(Group)
    active = models.BooleanField(default=True)
    permissions = models.ManyToManyField(
        Permission, 
        limit_choices_to={
        'content_type__app_label': 'subscriptions',
        'codename__in': [x[0] for x in SUBSCRIPTION_PERMISSIONS],
        }
    )
    stripe_id = models.CharField(max_length=120, blank=True, null=True)
    order = models.IntegerField(default=-1, help_text='Order of the price in the price page')
    featured = models.BooleanField(default=True, help_text='Featured Price on landing page')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    features = models.TextField(help_text='Comma separated list of features', blank=True, null=True)


    def save(self, *args, **kwargs):
        if not self.stripe_id:
            stripe_id = helpers.billing.create_product(
                name=self.name,
                metadata={
                    'subscription_plan_id': self.id,
                    },
                raw=False
            )
            self.stripe_id = stripe_id
        super().save(*args, **kwargs)

    def get_features_as_list(self):
        return [x.strip() for x in self.features.split('\n')] if self.features else []

    def __str__(self):
        return f'{self.name}'

    class Meta:
        permissions = SUBSCRIPTION_PERMISSIONS
        ordering = ['order', 'featured', '-updated']


class SubscriptionPrice(models.Model):
    '''
    Stripe Price - Subscription prices for different plans.
    '''
    class IntervalChoices(models.TextChoices):
        MONTHLY = 'month', 'Monthly'
        YEARLY = 'year', 'Yearly'
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    stripe_id = models.CharField(max_length=120, blank=True, null=True)
    interval = models.CharField(max_length=120, 
                                default=IntervalChoices.MONTHLY, 
                                choices=IntervalChoices.choices)
    
    price = models.DecimalField(max_digits=10, decimal_places=2, default=99.99)
    order = models.IntegerField(default=-1, help_text='Order of the price in the price page')
    featured = models.BooleanField(default=True, help_text='Featured Price on landing page')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    features = models.TextField(help_text='Comma separated list of features', blank=True, null=True)

    class Meta:
        ordering = ['subscription__order', 'order', 'featured', '-updated']
    
    def get_checkout_url(self):
        return reverse('sub-price-checkout', kwargs={'price_id': self.id})

    @property
    def stripe_currency(self):
        return 'usd'
    
    @property
    def stripe_price(self):
        '''
        Remove the decimal point and convert to cents.
        For example, 99.99 becomes 9999.
        '''
        return int(self.price * 100)

    @property
    def product_stripe_id(self):
        if not self.subscription:
            return None
        return self.subscription.stripe_id

    @property
    def display_sub_name(self):
        return self.subscription.name if self.subscription else 'Plan'
    
    @property
    def display_price_obj(self):
        return self.price
    
    @property
    def display_sub_subtitle(self):
        return self.subscription.subtitle if self.subscription else 'Plan Subtitle'
    
    def display_features_list(self):
        return self.subscription.get_features_as_list() if self.subscription else []
    
    def save(self, *args, **kwargs):
        if (not self.stripe_id and self.product_stripe_id is not None):
            stripe_id = helpers.billing.create_price(
            currency = self.stripe_currency,
            unit_amount = self.stripe_price,
            interval=self.interval,
            product = self.product_stripe_id,
            metadata={
                'subscription_plan_price_id': self.id,
            },
            raw=False
            )
            self.stripe_id = stripe_id
        super().save(*args, **kwargs)

        if self.featured and self.subscription:
            qs = SubscriptionPrice.objects.filter(
                subscription=self.subscription,
                interval=self.interval,
            ).exclude(id=self.id)
            qs.update(featured=False)

class SubscriptionStatus(models.TextChoices):
        ACTIVE = 'active', 'Active'
        TRIALING = 'trialing', 'Trialing'
        INCOMPLETE = 'incomplete', 'Incomplete'
        INCOMPLETE_EXPIRED = 'incomplete_expired', 'Incomplete Expired'
        PAST_DUE = 'past_due', 'Past Due'
        CANCELED = 'canceled', 'Canceled'
        UNPAID = 'unpaid', 'Unpaid'
        PAUSED = 'paused', 'Paused'

class UserSubscriptionQuerySet(models.QuerySet):
    def by_active_trialing(self):
            active_qs_loookup = (Q(status = SubscriptionStatus.ACTIVE) | Q(status = SubscriptionStatus.TRIALING))
            return self.filter(active_qs_loookup)

    def by_user_ids(self, user_ids=None):
        qs = self
        if isinstance(user_ids, list):
            qs = self.filter(user_id__in=user_ids)
        elif isinstance(user_ids, int):
            qs = self.qs.filter(user_id=[user_ids])
        elif isinstance(user_ids, str):
            qs = self.qs.filter(user_id=[user_ids])
        return qs

class UserSubscriptionManager(models.Manager):
    def get_queryset(self):
        return UserSubscriptionQuerySet(self.model, using=self._db)

    # def by_user_ids(self, user_ids=None):
    #     return self.get_queryset().by_user_ids(user_ids=user_ids)
        


class UserSubscription(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)
    user_cancelled = models.BooleanField(default=False)
    stripe_id = models.CharField(max_length=120, blank=True, null=True)
    original_period_start = models.DateTimeField(auto_now = False, auto_now_add=False, blank=True, null=True)
    current_period_start = models.DateTimeField(auto_now = False, auto_now_add=False, blank=True, null=True)
    current_period_end = models.DateTimeField(auto_now = False, auto_now_add=False, blank=True, null=True)
    cancel_at_period_end = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=SubscriptionStatus.choices, blank=True, null=True)

    objects = UserSubscriptionManager()
    
    def get_absolute_url(self):
        return reverse("user_subscription")
    
    def get_cancel_url(self):
        return reverse("user_subscription_cancel")
    
    @property
    def is_active_status(self):
        return self.status in [
            SubscriptionStatus.ACTIVE,
            SubscriptionStatus.TRIALING,
        ] 
    
    @property
    def plan_name(self):
        return self.subscription.name if self.subscription else None

    def serialize(self):
        return{
            'plan_name': self.plan_name,
            'status': self.status,
            'current_period_start': self.current_period_start,
            'current_period_end': self.current_period_end,
        }

    @property
    def billing_cycle_anchor(self):
        """
        Optional delay to start new sub in stripe checkout.
        """
        if self.current_period_end:
            if not self.current_period_end:
                return None
            return int(self.current_period_end.timestamp())

    def save(self, *args, **kwargs):
        if (self.original_period_start is None and self.current_period_start is not None):
            self.original_period_start = self.current_period_start
        super().save(*args, **kwargs)

def user_sub_post_save(sender, instance, *args, **kwargs):
    user_sub_instance = instance
    user = user_sub_instance.user
    subscription_obj = user_sub_instance.subscription
    groups_ids = []
    if subscription_obj is not None:
        groups = subscription_obj.groups.all()
        groups_ids = groups.values_list('id', flat=True)
    if not ALLOW_CUSTOM_GROUPS:
        user.groups.set(groups)
    else:
        subs_qs = Subscription.objects.filter(active=True)
        if subscription_obj is not None:
            subs_qs = subs_qs.exclude(id=subscription_obj.id)
        subs_groups = subs_qs.values_list('groups__id', flat=True)
        subs_groups_set = set(subs_groups)
        current_groups = user.groups.all().values_list('id', flat=True)
        groups_ids_set = set(groups_ids)
        current_groups_set = set(current_groups) - subs_groups_set
        final_group_ids = list(groups_ids_set | current_groups_set)
        user.groups.set(final_group_ids)

post_save.connect(user_sub_post_save, sender=UserSubscription)