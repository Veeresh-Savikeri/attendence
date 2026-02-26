from django.http import HttpResponse
import qrcode
from io import BytesIO
from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from teacher.models import *



# Create your views here.
def home(request):
    return render(request,"home.html")



def register_view(request):
    if request.method =="POST":  
       username = request.POST.get("name")
       gender = request.POST.get("gender")
       email = request.POST.get("email")
       phoneno = request.POST["phoneno"]
       country = request.POST.get("country")
       state = request.POST.get("state")
       district = request.POST.get("district")
       address = request.POST.get("address")
       password = request.POST.get("password")
       print(type(phoneno))
         # Create User
       # create base User (username, email, password only)
       user = User.objects.create_user(
           username=username,
           email=email,
           password=password
       )
       # create associated Profile with additional fields
       Profile.objects.create(
           user=user,
           gender=gender,
           phoneno=phoneno,
           country=country,
           state=state,
           district=district,
           address=address
       )
    return render(request,"register.html")

@login_required
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)   # creates session
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid Username or Password")
    return render(request, "login.html")

@login_required    
def dashboard(request):
    student = Profile.objects.get(user=request.user)
    # records = Attendance.objects.filter(student=student).order_by('-date')
    total = Attendance.objects.filter(student=student).count() 
    details = Attendance.objects.filter(student=student)
    
    
    return render(request,"dashboard.html",{'records': total,"details":details})
    
    
@login_required
def student_qr(request):
    student = Profile.objects.get(user=request.user)
    qr_data = f"http://127.0.0.1:8000/teacher/mark-attendance/{student.id}/"
    qr = qrcode.make(qr_data)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    return HttpResponse(buffer.getvalue(), content_type="image/png")
