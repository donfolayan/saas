from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username'] or None
        password = request.POST['password'] or None
        if all([username, password]):
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    return render(request, 'auth/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username'] or None
        email = request.POST['email'] or None
        password = request.POST['password'] or None

        username_exists = User.objects.filter(username__iexact=username).exists()
        email_exists = User.objects.filter(email__iexact=email).exists()

        if username_exists==0 or email_exists==0:
            User.objects.create_user(username=username, email=email, password=password)
            return redirect('/login/')
        print('User already exists')
    
    return render(request, 'auth/register.html')