from typing import Any
import helpers.billing
from django.db.models import Q
from customers.models import Customer
from subscriptions.models import UserSubscription, Subscription, SubscriptionStatus

def refresh_active_user_subscriptions(user_ids=None, active_only=True, verbose=False):
    
    qs = UserSubscription.objects.all()
    qs = qs.by_active_trialing() if active_only else qs
    qs = qs.by_user_ids(user_ids=user_ids) if user_ids is not None else qs
    
    complete_count = 0
    qs_count = qs.count()

    for obj in qs:
        if verbose:
            print(f'Updating {obj.user} - {obj.stripe_id} - {obj.subscription} - {obj.current_period_end}')
        if obj.stripe_id and obj.is_active_status:
            sub_data = helpers.billing.cancel_subscription(
                obj.stripe_id, 
                reason='User wanted to end', 
                feedback='other',
                cancel_at_period_end=True,
                raw=False)

            for k, v in sub_data.items():
                setattr(obj, k, v)
            obj.save()
            complete_count += 1
    return complete_count == qs_count

def clear_dangling_subs():
    qs = Customer.objects.filter(stripe_id__isnull=False)
    for customer_obj in qs:
        user = customer_obj.user
        customer_stripe_id = customer_obj.stripe_id
        print(f'Sync {user} - {customer_stripe_id} subs and remove old ones')
        

        subs = helpers.billing.get_customer_active_subscriptions(customer_stripe_id)
        for sub in subs:
            existing_user_subs_qs = UserSubscription.objects.filter(stripe_id__iexact= f'{sub.id}'.strip())
            if existing_user_subs_qs.exists():
                continue
            helpers.billing.cancel_subscription(sub.id, reason='Dangling active subscription', cancel_at_period_end=False)
            print(sub.id, existing_user_subs_qs.exists())

def sync_sub_group_permissions():
    qs = Subscription.objects.filter(active=True)
    for obj in qs:
        sub_perms = obj.permissions.all()
        for group in obj.groups.all():
            group.permissions.set(sub_perms)
        
