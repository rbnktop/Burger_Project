from django.urls import path
from .views import home_view, login_view, logout_view, history_sidebar

app_name = "greeting"

urlpatterns = [
    path("", home_view, name="home"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("history-sidebar/", history_sidebar, name="history_sidebar"),
]
