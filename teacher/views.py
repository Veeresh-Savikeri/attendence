from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from home.models import *
from django.contrib.auth import authenticate, login
from .models import *
from datetime import date
from django.http import JsonResponse
import json





@login_required
def staff_dashboard(request):
    session = Session.objects.all()
    return render(request, 'staff_dashboard.html',context={"sessions":session})


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



def mark_attendance(request):
    if request.method == "POST":
        data = json.loads(request.body)
        student_id = data.get("student_id")
        session_id = data.get("session_id")
        print(student_id, session_id)
        student = Profile.objects.get(id = student_id)
        session = Session.objects.get(id = session_id)
        print(student,session)
        if Attendance.objects.filter(student=student,session=session,date=date.today()).exists():
            return JsonResponse({"data":f"{student.user.username} your attendance already done"})
        Attendance.objects.create(student=student,session = session)
        
            
    return JsonResponse({"data":f"{student.user.username}"})


def session(request):
    if request.method == "POST":
        batchcode = request.POST.get("batch_code")
        subject =request.POST.get("subject") 
        branch = request.POST.get("branch")
        trainer = request.POST.get("trainer")
        mode =request.POST.get("mode")
        print(batchcode,subject,branch,trainer,mode)
        if batchcode and subject and branch and trainer and mode:
            Session.objects.create(
                batchcode = batchcode,
                subject =subject,
                branch =branch,
                trainer =trainer,
                mode = mode
            )
            return redirect("http://127.0.0.1:8000/teacher/staff-dashboard")
        else:
            messages.error(request, "All fields are required.")
    return render(request,"session.html")

def scan(request,session_id):
    
    return render(request,"scan.html",context={"session_id":session_id})