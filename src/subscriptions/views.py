import helpers.billing
from django.shortcuts import render, redirect
from django.urls import reverse
from subscriptions.models import SubscriptionPrice, UserSubscription
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
@login_required
def user_subscription_view(request, *args, **kwargs):
    user_sub_obj, created = UserSubscription.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        if user_sub_obj.stripe_id:
            sub_data = helpers.billing.get_subscription(user_sub_obj.stripe_id, raw=False)

            for k, v in sub_data.items():
                setattr(user_sub_obj, k, v)
            user_sub_obj.save()
        messages.success(request, 'Your subscription has been updated.')
        return redirect(user_sub_obj.get_absolute_url())
    
    return render(request, 'subscriptions/user_detail_view.html', {'subscription': user_sub_obj})

@login_required
def user_subscription_cancel_view(request, *args, **kwargs):
    user_sub_obj, created = UserSubscription.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        print('refresh sub')
        if user_sub_obj.stripe_id and user_sub_obj.is_active_status:
            sub_data = helpers.billing.cancel_subscription(
                user_sub_obj.stripe_id, 
                reason='User wanted to end', 
                feedback='other',
                cancel_at_period_end=True,
                raw=False)

            for k, v in sub_data.items():
                setattr(user_sub_obj, k, v)
            user_sub_obj.save()
            messages.success(request, 'Your subscription has been cancelled.')
        return redirect(user_sub_obj.get_absolute_url())
    
    return render(request, 'subscriptions/user_cancel_view.html', {'subscription': user_sub_obj})
     


def subscription_price_view(request, interval='month'):
    qs = SubscriptionPrice.objects.filter(featured=True)
    inv_month = SubscriptionPrice.IntervalChoices.MONTHLY
    inv_year = SubscriptionPrice.IntervalChoices.YEARLY
    url_path_name = 'pricing_interval'
    monthly_url = reverse(url_path_name, kwargs={'interval': inv_month})
    yearly_url = reverse(url_path_name, kwargs={'interval': inv_year})
    object_list = qs.filter(interval = inv_month) if interval == inv_month else qs.filter(interval = inv_year)
    active = inv_month if interval == inv_month else inv_year
    
    return render(request, 'subscriptions/pricing.html',{
        'object_list': object_list,
        'monthly_url': monthly_url,
        'yearly_url': yearly_url,
        'active': active,})