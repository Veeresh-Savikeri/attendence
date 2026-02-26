from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from home.models import *
from django.contrib.auth import authenticate, login
from .models import *
from datetime import date





@login_required
def staff_dashboard(request):
    return render(request, 'staff_dashboard.html')

# def staff_register(request):
    # if request.method == "POST":
    #     username = request.POST.get("username")
    #     password = request.POST.get("password")
    #     email = request.POST.get("email")

    #     if User.objects.filter(username=username).exists():
    #         messages.error(request, "Username already exists")
    #         return redirect("staff_register")

    #     user = User.objects.create_user(
    #         username=username,
    #         password=password,
    #         email=email
    #     )

    #     user.is_staff = True   # 🔥 Important
    #     user.save()

    #     messages.success(request, "Staff Registered Successfully")
    #     return redirect("staff-login")

    # return render(request, "staff_register.html")

def staff_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Check if user is staff
            if Staff.objects.filter(user=user).exists():
                login(request, user)
                return redirect('staff_dashboard')
            else:
                messages.error(request, "You are not authorized as staff.")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'staff_login.html')



def mark_attendance(request, student_id):
    student = Profile.objects.get(id=student_id)

    # determine current logged-in staff
    try:
        current_staff = Staff.objects.get(user=request.user)
    except Staff.DoesNotExist:
        return HttpResponse("Current user is not registered as staff", status=403)

    # Prevent duplicate attendance same day
    if Attendance.objects.filter(student=student, staff=current_staff, date=date.today()).exists():
        return HttpResponse("Already Marked Today")
    Attendance.objects.create(student=student, staff=current_staff)
    return HttpResponse("Attendance Marked Successfully")