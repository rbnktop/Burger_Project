from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib import messages


def home_view(request):
    return render(request, "home.html")


def login_view(request):

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("greeting:home")
        return render(request, "login.html", {"form": form}, status=422)
    else:
        form = AuthenticationForm()

    # CRITICAL: This print should trigger ONLY after a failed POST
    if request.method == "POST":
        print(f"FAILED LOGIN ERRORS: {form.errors}")

    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("greeting:home")
