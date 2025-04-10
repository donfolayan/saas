from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()

@login_required
def profile_list_view(request, *args, **kwargs):
    user = request.user
    context = {
        'object_list': User.objects.filter(is_active=True)
    }
    return render(request, 'profiles/list.html', context)

@login_required
def profile_detail_view(request, username=None, *args, **kwargs):
    user = request.user
    user_groups = user.groups.all()
    # print(user_groups)
    # if user_groups.filter(name__icontains='basic').exists():
    #     return HttpResponse("You do not have permission to view this page")
    profile_user_obj = get_object_or_404(User, username=username)
    is_me = user == profile_user_obj
    context = {
        'object': profile_user_obj,
        'instance': profile_user_obj,
        'owner': is_me,
    }

    return render(request, 'profiles/detail.html', context)