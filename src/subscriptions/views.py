from django.shortcuts import render
from django.urls import reverse
from subscriptions.models import SubscriptionPrice

# Create your views here.
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