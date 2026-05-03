from django.http import HttpResponse
import qrcode
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from teacher.models import *
from datetime import datetime
from collections import defaultdict


# Create your views here.
def home(request):
    return render(request, "home.html")


def register_view(request):
    if request.method == "POST":  
        username = request.POST.get("name")
        gender = request.POST.get("gender")
        email = request.POST.get("email")
        phoneno = request.POST.get("phoneno")
        country = request.POST.get("country")
        state = request.POST.get("state")
        district = request.POST.get("district")
        address = request.POST.get("address")
        password = request.POST.get("password")
        
        # Validate required fields
        if not all([username, gender, email, phoneno, country, state, district, address, password]):
            messages.error(request, "All fields are required.")
            return render(request, "register.html")
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "register.html")
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, "register.html")
        
        try:
            # Create base User
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            # Create associated Profile with additional fields
            Profile.objects.create(
                user=user,
                gender=gender,
                phoneno=phoneno,
                country=country,
                state=state,
                district=district,
                address=address
            )
            messages.success(request, "Registration successful! Please login.")
            return redirect('login')
        except Exception as e:
            messages.error(request, f"Registration failed: {str(e)}")
            
    return render(request, "register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Username and password are required.")
            return render(request, "login.html")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, "login.html")


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')

    
@login_required(login_url='login')
def student_qr(request):
    try:
        student = Profile.objects.get(user=request.user)
        # Use only student id for QR code, no hardcoded data
        qr_data = str(student.id)
        qr = qrcode.make(qr_data)
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        buffer.seek(0)
        return HttpResponse(buffer.getvalue(), content_type="image/png")
    except Profile.DoesNotExist:
        messages.error(request, "Student profile not found.")
        return redirect('dashboard')

    
@login_required(login_url='login')
def dashboard(request):
    try:
        profile = Profile.objects.get(user=request.user)
        date = datetime.now().date()
        time = datetime.now().strftime("%H:%M:%S")
        context = {
            "profile": profile,
            "date": date,
            "time": time
        }
        return render(request, "dashboard.html", context)
    except Profile.DoesNotExist:
        messages.error(request, "Student profile not found.")
        return redirect('login')

    
@login_required(login_url='login')
def attendance(request):
    profile = Profile.objects.get(user=request.user)
    records = Attendance.objects.filter(student=profile).select_related('student','session')
   
    session_students = defaultdict(list)
    for record in records:
        session_students[record.session.batchcode].append(record)   

    session_students = dict(session_students)
 
    context = {        
        "session_attendance":session_students,
        "date": datetime.now().date(),
        "time": datetime.now().strftime("%H:%M:%S")
    }
    return render(request, "attendence.html", context)

def stu_details(request):
    student = Profile.objects.get(user = request.user.id)
    

    
    return render(request,"stu_details.html",context={"student":student})