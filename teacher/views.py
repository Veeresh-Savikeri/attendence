from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def staff_dashboard(request):
    return render(request, 'staff_dashboard.html')

def staff_register(request):
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

    return render(request, "staff_register.html")


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Staff

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