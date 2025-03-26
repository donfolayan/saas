import pathlib
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from visits.models import PageVisits

LOGIN_URL = settings.LOGIN_URL

def home_view(request, *args, **kwargs):
    qs = PageVisits.objects.all()
    page_qs = PageVisits.objects.filter(path=request.path)
    try:
        percent_visit = (page_qs.count()/qs.count())*100
    except ZeroDivisionError:
        percent_visit = 0
    my_title = "Homepage"
    my_context = {
        'page_title' : my_title,
        'total_visit_count' : qs.count(),
        'page_visit_count' : page_qs.count(),
        'percent_visit': percent_visit,
    }
    PageVisits.objects.create(path=request.path)
    html_template  = "home.html"
    return render(request, html_template, my_context)

def about_view(request, *args, **kwargs):
    qs = PageVisits.objects.all()
    page_qs = PageVisits.objects.filter(path=request.path)
    try:
        percent_visit = round((page_qs.count()/qs.count())*100, 2)
    except ZeroDivisionError:
        percent_visit = 0
    my_title = "Homepage"
    my_context = {
        'page_title' : my_title,
        'total_visit_count' : qs.count(),
        'page_visit_count' : page_qs.count(),
        'percent_visit': percent_visit,
    }
    PageVisits.objects.create(path=request.path)
    html_template  = "home.html"
    return render(request, html_template, my_context)

VALID_CODE = 'abc123'

def pw_protected_view(request, *args, **kwargs):
    is_allowed = request.session.get('protected_page_allowed') or 0

    if request.method == 'POST':
        user_pw_sent=request.POST.get('code') or None
        if user_pw_sent == VALID_CODE:
            is_allowed = 1
            request.session['protected_page_allowed'] = is_allowed

    if is_allowed:
        return render(request, 'protected/view.html', {})
    return render(request, 'protected/entry.html')

@login_required
def user_required_view(request, *args, **kwargs):
    return render(request, 'protected/user-required.html', {})

@staff_member_required(login_url=LOGIN_URL)
def staff_required_view(request, *args, **kwargs):
    return render(request, 'protected/staff-required.html', {})