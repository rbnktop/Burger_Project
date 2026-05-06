from django.urls import path
from .views import home_view, login_view

urlpatterns = [
    path('home/', home_view, name='home'),
    path('', login_view, name='login'),
]