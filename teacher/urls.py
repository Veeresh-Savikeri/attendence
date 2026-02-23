from django.urls import path
from .views import *
urlpatterns = [
    path('staff-register/', staff_register, name='staff_register'),
    path('staff-login/', staff_login, name='staff_login'),
    path('staff-dashboard/', staff_dashboard, name='staff_dashboard'),
]
