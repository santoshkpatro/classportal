from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from . models import User
from . forms import LoginForm, RegisterForm


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if not form.is_valid():
            messages.warning(request, 'Invalid form details')
            return render(request, 'accounts/register.html')
        
        new_user_credentials = form.cleaned_data
        password = new_user_credentials.pop('password')
        confirm_password = new_user_credentials.pop('confirm_password')

        if password != confirm_password:
            messages.warning(request, 'Password and confirm password are not same')
            return redirect('index')

        new_user = User(**new_user_credentials)
        new_user.set_password(password)
        new_user.save()
        return redirect('index')

    return render(request, 'accounts/register.html')
        


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if not form.is_valid():
            messages.warning(request, 'Invalid form details')
            return render(request, 'accounts/login.html')
    
        user = authenticate(**form.cleaned_data)
        if not user:
            messages.warning(request, 'Invalid user credentials')
            return render(request, 'accounts/login.html')
        
        login(request, user)
        return redirect('index')
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('index')