from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

User = get_user_model()


# Create your views here.
@login_required
def profile_view(request, username=None, *args, **kwargs):
    user = request.user
    profile_user_obj = get_object_or_404(User, username=username)
    is_me = user == profile_user_obj
    return HttpResponse(f'Hello {username} - {profile_user_obj.id} - {is_me}')