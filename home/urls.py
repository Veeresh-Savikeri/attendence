from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    path('student-qr/', student_qr, name='student_qr'),
    path("dashboard/", dashboard, name="dashboard"),
    path("attendance/", attendance, name="attendence"),
    path("stu-details/",stu_details, name="student_details")
]
