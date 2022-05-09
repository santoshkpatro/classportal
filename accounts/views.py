from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from . forms import LoginForm


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