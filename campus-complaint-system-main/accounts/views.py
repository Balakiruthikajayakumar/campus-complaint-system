from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User

# Complaint Model
from complaints.models import Complaint


# =====================================
# HOME PAGE
# =====================================
def home(request):
    return render(request, 'home.html')


# =====================================
# REGISTER USER
# =====================================
def register_user(request):

    if request.method == 'POST':

        # ✅ NEW: Get Email from form
        email = request.POST.get('email')

        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        department = request.POST.get('department')
        year = request.POST.get('year')
        section = request.POST.get('section')

        # Prevent duplicate username
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists ❌")
            return redirect('register')

        # ✅ NEW: Prevent duplicate email
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists ❌")
            return redirect('register')

        # Create User
        User.objects.create_user(
            username=username,
            email=email,  # ✅ ADDED EMAIL HERE
            password=password,
            role=role,
            department=department,
            year=year,
            section=section
        )

        messages.success(request, "Registration Successful ✅")
        return redirect('login')

    return render(request, 'register.html')


# =====================================
# LOGIN USER
# =====================================
def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            # ROLE BASED REDIRECT
            if user.role == 'student':
                return redirect('student_homepage')

            elif user.role == 'tutor':
                return redirect('tutor_homepage')

            elif user.role == 'hod':
                return redirect('hod_homepage')

            elif user.role == 'principal':
                return redirect('principal_homepage')

            else:
                return redirect('/admin/')

        else:
            messages.error(request,
                           "Invalid Username or Password ❌")

    return render(request, 'login.html')


# =====================================
# LOGOUT
# =====================================
def user_logout(request):
    logout(request)
    return redirect('login')


# =====================================
# STUDENT HOMEPAGE
# =====================================
@login_required
def student_home(request):

    total = Complaint.objects.filter(
        student=request.user
    ).count()

    pending = Complaint.objects.filter(
        student=request.user
    ).exclude(status='resolved').count()

    resolved = Complaint.objects.filter(
        student=request.user,
        status='resolved'
    ).count()

    context = {
        "total_count": total,
        "pending_count": pending,
        "resolved_count": resolved
    }

    return render(
        request,
        'student_homepage.html',
        context
    )


# =====================================
# TUTOR HOMEPAGE
# =====================================
@login_required
def tutor_home(request):

    pending = Complaint.objects.filter(
        status='submitted'
    ).count()

    approved = Complaint.objects.filter(
        status='tutor_approved'
    ).count()

    context = {
        "pending_count": pending,
        "approved_count": approved
    }

    return render(
        request,
        'tutor_homepage.html',
        context
    )


# =====================================
# HOD HOMEPAGE
# =====================================
@login_required
def hod_home(request):

    pending = Complaint.objects.filter(
        status='tutor_approved'
    ).count()

    approved = Complaint.objects.filter(
        status='hod_approved'
    ).count()

    context = {
        "pending_count": pending,
        "approved_count": approved
    }

    return render(
        request,
        'hod_homepage.html',
        context
    )


# =====================================
# PRINCIPAL HOMEPAGE
# =====================================
@login_required
def principal_home(request):

    pending = Complaint.objects.filter(
        status='hod_approved'
    ).count()

    resolved = Complaint.objects.filter(
        status='resolved'
    ).count()

    rejected = Complaint.objects.filter(
        status='rejected'
    ).count()

    context = {
        "pending_count": pending,
        "resolved_count": resolved,
        "rejected_count": rejected
    }

    return render(
        request,
        'principal_homepage.html',
        context
    )
