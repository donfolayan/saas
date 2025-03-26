import pathlib
from django.http import HttpResponse
from django.shortcuts import render
from visits.models import PageVisits


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

def pw_protected_view(request, *args, **kwargs):
    is_allowed = False
    
    return render(request, 'protected/entry.html')