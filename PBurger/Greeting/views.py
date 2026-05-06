from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def home_view(request):
    return render(request, 'home.html')

def login_view(request):
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        
        user = authenticate(request, username=u, password=p)
        
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, "Usuario ou senha invalidos.")
            
    return render(request, 'login.html')