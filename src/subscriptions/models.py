from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_save

User = settings.AUTH_USER_MODEL

SUBSCRIPTION_PERMISSIONS = [
            ('advanced', 'Advanced Perm'),
            ('pro', 'Pro Perm'),
            ('basic', 'Basic Perm'),
            ('basic ai', 'Basic AI Perm'),
        ]

class Subscription(models.Model):
    name = models.CharField(max_length=120)
    groups = models.ManyToManyField(Group)
    active = models.BooleanField(default=True)
    permissions = models.ManyToManyField(
        Permission, 
        limit_choices_to={
        'content_type__app_label': 'subscriptions',
        'codename__in': [x[0] for x in SUBSCRIPTION_PERMISSIONS],
        }
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        permissions = SUBSCRIPTION_PERMISSIONS

class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True)
    active = models.BooleanField(default=True)
