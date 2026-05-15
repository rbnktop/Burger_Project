from itertools import chain
from operator import attrgetter

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from Inventory.models import Stock
from Cashier.models import Order
from Menu.models import Product


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

    stock_hist = Stock.history.all()  # type: ignore
    product_hist = Product.history.all()  # type: ignore
    order_hist = Order.history.all()  # type: ignore

    list = sorted(
        chain(stock_hist, product_hist, order_hist),
        key=attrgetter("history_date"),
        reverse=True,
    )

    return render(request, "history_sidebar.html", {"history": list})
