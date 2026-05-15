from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from Inventory.models import Stock
from Cashier.models import Order


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

    if request.method == "POST":
        print(f"FAILED LOGIN ERRORS: {form.errors}")

    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("greeting:home")


def history_sidebar(request):
    """
    Fetches the latest changes across the app and returns only the sidebar HTML.
    """
    # django-simple-history creates a separate table for each model.
    # To get a global feed, we fetch the latest from the models we care about:
    recent_stock = Order.history.all()  # type: ignore

    # If you also tracked Burger:
    # recent_burgers = Burger.history.all()[:10]

    # Combine and sort them by date (newest first)
    # history_list = sorted(
    #     chain(recent_stock, recent_burgers),
    #     key=attrgetter('history_date'),
    #     reverse=True
    # )[:10]

    # For now, let's just use Stock to keep it simple:
    history_list = recent_stock

    return render(request, "history_sidebar.html", {"history": recent_stock})
