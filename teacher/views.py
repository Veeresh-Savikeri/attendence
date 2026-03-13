from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from home.models import *
from django.contrib.auth import authenticate, login, logout
from .models import *
from datetime import date
import json


@login_required(login_url='staff_login')
def staff_dashboard(request):
    try:
        # Verify user is staff
        if not Staff.objects.filter(user=request.user).exists():
            messages.error(request, "You are not authorized as staff.")
            return redirect('staff_login')
        
        sessions = Session.objects.all()
        return render(request, 'staff_dashboard.html', context={"sessions": sessions})
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect('staff_login')


def staff_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, "Username and password are required.")
            return render(request, 'staff_login.html')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Check if user is staff
            if Staff.objects.filter(user=user).exists():
                login(request, user)
                return redirect('staff_dashboard')
            else:
                messages.error(request, "You are not authorized as staff.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'staff_login.html')


@login_required(login_url='staff_login')
def staff_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('staff_login')


@require_http_methods(["POST"])
@csrf_exempt
def mark_attendance(request):
    try:
        data = json.loads(request.body)
        student_id = data.get("student_id")
        session_id = data.get("session_id")
        
        if not student_id or not session_id:
            return JsonResponse({"error": "Student ID and Session ID are required."}, status=400)
        
        try:
            student = Profile.objects.get(id=student_id)
            session = Session.objects.get(id=session_id)
        except Profile.DoesNotExist:
            return JsonResponse({"error": "Student not found."}, status=404)
        except Session.DoesNotExist:
            return JsonResponse({"error": "Session not found."}, status=404)
        
        # Check if attendance already marked
        if Attendance.objects.filter(student=student, session=session, date=date.today()).exists():
            return JsonResponse({"data": f"{student.user.username} your attendance is already marked today."})
        
        # Create new attendance record
        Attendance.objects.create(student=student, session=session)
        return JsonResponse({"data": f"Attendance marked for {student.user.username}"})
        
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON."}, status=400)
    except Exception as e:
        return JsonResponse({"error": f"Error: {str(e)}"}, status=500)


@login_required(login_url='staff_login')
@require_http_methods(["GET", "POST"])
def session(request):
    try:
        # Verify user is staff
        if not Staff.objects.filter(user=request.user).exists():
            messages.error(request, "You are not authorized as staff.")
            return redirect('staff_login')
        
        if request.method == "POST":
            batchcode = request.POST.get("batch_code", "").strip()
            subject = request.POST.get("subject", "").strip()
            branch = request.POST.get("branch", "").strip()
            trainer = request.POST.get("trainer", "").strip()
            mode = request.POST.get("mode", "").strip()
            
            if not all([batchcode, subject, branch, trainer, mode]):
                messages.error(request, "All fields are required.")
                return render(request, "session.html")
            
            Session.objects.create(
                batchcode=batchcode,
                subject=subject,
                branch=branch,
                trainer=trainer,
                mode=mode
            )
            messages.success(request, "Session created successfully.")
            return redirect('staff_dashboard')
        
        return render(request, "session.html")
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return render(request, "session.html")


@login_required(login_url='staff_login')
def scan(request, session_id):
    try:
        # Verify user is staff
        if not Staff.objects.filter(user=request.user).exists():
            messages.error(request, "You are not authorized as staff.")
            return redirect('staff_login')
        
        session = Session.objects.get(id=session_id)
        return render(request, "scan.html", context={"session_id": session_id, "session": session})
    except Session.DoesNotExist:
        messages.error(request, "Session not found.")
        return redirect('staff_dashboard')
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect('staff_dashboard')
