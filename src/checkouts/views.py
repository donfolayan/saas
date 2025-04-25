import helpers.billing
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from subscriptions.models import SubscriptionPrice, Subscription, UserSubscription


User = get_user_model()

BASE_URL = settings.BASE_URL

# Create your views here.
def product_price_redirect_view(request, price_id=None, *args, **kwargs):
    request.session['checkout_subscription_price_id'] = price_id
    return redirect('stripe-checkout-start')

@login_required
def checkout_redirect_view(request):
    checkout_subscription_price_id = request.session.get('checkout_subscription_price_id')
    try:
        obj = SubscriptionPrice.objects.get(id=checkout_subscription_price_id)
    except:
        obj = None
    if checkout_subscription_price_id is None or obj is None:
        return redirect('pricing')
    customer_stripe_id = request.user.customer.stripe_id
    print(customer_stripe_id)

    success_url_path = reverse('stripe-checkout-end')
    pricing_url_path = reverse('pricing')
    success_url = f'{BASE_URL}{success_url_path}'
    cancel_url = f'{BASE_URL}{pricing_url_path}'
    price_stripe_id = obj.stripe_id

    url = helpers.billing.start_checkout_session(
        customer_id=customer_stripe_id,
        success_url=success_url,
        cancel_url=cancel_url,
        price_stripe_id=price_stripe_id,
        raw=False,
    )

    return redirect(url)

def checkout_finalize_view(request):
    session_id = request.GET.get('session_id')
    if session_id is None:
        return redirect('home')
    checkout_data = helpers.billing.get_checkout_customer_plan(session_id)
    plan_id = checkout_data.pop('plan_id')
    customer_id = checkout_data.pop('customer_id')
    sub_stripe_id = checkout_data.pop('sub_stripe_id')
    subscription_data = {**checkout_data}

    try:
        sub_obj = Subscription.objects.get(subscriptionprice__stripe_id=plan_id)
    except:
        sub_obj = None

    try:
        user_obj = User.objects.get(customer__stripe_id=customer_id)
    except:
        user_obj = None
    
    _user_sub_exists = False
    updated_sub_options = {
        'subscription': sub_obj,
        'stripe_id': sub_stripe_id,
        'user_cancelled': False,
        **subscription_data,
    }
    try:
        _user_sub_obj = UserSubscription.objects.get(user = user_obj)
        _user_sub_exists = True
    except UserSubscription.DoesNotExist:
        _user_sub_obj = UserSubscription.objects.create(user = user_obj, **updated_sub_options)
    except:
        _user_sub_obj = None

    if _user_sub_exists:
        #cancel the old subscription
        old_stripe_id = _user_sub_obj.stripe_id
        same_stripe_id = sub_stripe_id == old_stripe_id
        if old_stripe_id is not None and not same_stripe_id:
            try:
                helpers.billing.cancel_subscription(old_stripe_id, reason='User changed subscription', feedback='other')
            except:
                pass
        
        #update the subscription
        for k, v in updated_sub_options.items():
            setattr(_user_sub_obj, k, v)
        _user_sub_obj.save()
        messages.success(request, "You've successfully purchased a subscription")
        return redirect(_user_sub_obj.get_absolute_url())

    if None in [user_obj, sub_obj, _user_sub_obj]:
        return HttpResponseBadRequest("There was an error with your account, please contact us.")

    context = {}
    return render(request, 'checkout/success.html', context)