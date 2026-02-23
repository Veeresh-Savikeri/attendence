from django.urls import path
from .views import *

urlpatterns = [
  path("",home,name="home"),
  path("login/",login_view ,name="login"),
  path("register/",register_view,name="register"),
  path("login/",login_view ,name="login"),
  path("dashboard/",dashboard ,name="dashboard"),
  path('student-qr/',student_qr, name='student_qr'),
  path('mark-attendance/<int:student_id>/', mark_attendance, name='mark_attendance'),

]
