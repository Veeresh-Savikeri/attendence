from django.urls import path
from .views import *

urlpatterns = [
    path('staff-login/', staff_login, name='staff_login'),
    path('staff-logout/', staff_logout, name='staff_logout'),
    path('staff-dashboard/', staff_dashboard, name='staff_dashboard'),
    path('mark-attendance/', mark_attendance, name='mark_attendance'),
    path('staff-dashboard/session/', session, name='session'),
    path('scan/<int:session_id>/', scan, name='scan'),
]
