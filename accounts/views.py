from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Import User Model
from .models import User

# Import Complaint / Leave / Outpass Models
from complaints.models import Complaint
from leave_form.models import LeaveForm
from outpass.models import Outpass


# =====================================
# HOME PAGE
# =====================================
def home(request):
    """
    Landing page of the website
    """
    return render(request, 'home.html')


# =====================================
# REGISTER USER
# =====================================
def register_user(request):

    if request.method == 'POST':

        # Get form data from HTML form
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        department = request.POST.get('department')
        year = request.POST.get('year')
        section = request.POST.get('section')

        # ⭐ FIX
        # If username is empty use name/email instead
        if not username:
            username = request.POST.get('name') or request.POST.get('email')

        # Prevent duplicate usernames
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists ❌")
            return redirect('register')

        # Create user
        User.objects.create_user(
            username=username,
            email=email,
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

        # Authenticate user
        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            # ROLE BASED REDIRECT
            if user.role.lower() == 'student':
                return redirect('student_homepage')

            elif user.role.lower() == 'tutor':
                return redirect('tutor_homepage')

            elif user.role.lower() == 'hod':
                return redirect('hod_homepage')

            elif user.role.lower() == 'principal':
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
# STUDENT DASHBOARD
# =====================================
@login_required
def student_home(request):

    """
    Student Dashboard Data
    """

    # Total complaints raised by this student
    total = Complaint.objects.filter(
        student=request.user
    ).count()

    # Complaints that are not resolved yet
    pending = Complaint.objects.filter(
        student=request.user
    ).exclude(status='resolved').count()

    in_progress = Complaint.objects.filter(
    student=request.user,
    status='tutor_approved'
    ).count()
    # Complaints that are resolved
    resolved = Complaint.objects.filter(
        student=request.user,
        status='resolved'
    ).count()

    # ⭐ Notification count
    complaint_notifications = Complaint.objects.filter(
        student=request.user
    ).exclude(status='submitted').count()

    leave_notifications = LeaveForm.objects.filter(
        student=request.user
    ).exclude(status='pending').count()

    outpass_notifications = Outpass.objects.filter(
        student=request.user
    ).exclude(status='pending').count()

    notification_count = (
        complaint_notifications +
        leave_notifications +
        outpass_notifications
    )
    
    # ⭐ Recent Complaints (latest 3)
    recent_complaints = Complaint.objects.filter(
        student=request.user
    ).order_by('-created_at')[:3]



    context = {
        "total_count": total,
        "pending_count": pending,
        "resolved_count": resolved,
        "in_progress_count":in_progress,
        "recent_complaints":recent_complaints

        # Send recent complaints to dashboard
    }

    return render(
        request,
        'student_homepage.html',
        context
    )


# =====================================
# MY REQUESTS PAGE
# Shows complaints + leave + outpass
# =====================================
@login_required
def my_requests(request):

    """
    This page shows all student requests in one place
    """

    # Student complaints
    complaints = Complaint.objects.filter(
        student=request.user
    )

    # Student leave requests
    leaves = LeaveForm.objects.filter(
        student=request.user
    )

    # Student outpass requests
    outpasses = Outpass.objects.filter(
        student=request.user
    )

    return render(request, "my_requests.html", {
        "complaints": complaints,
        "leaves": leaves,
        "outpasses": outpasses
    })


# =====================================
# TUTOR DASHBOARD
# =====================================
@login_required
def tutor_home(request):

    """
    Tutor dashboard shows complaints submitted by students
    """

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
# HOD DASHBOARD
# =====================================
@login_required
def hod_home(request):

    """
    HOD dashboard shows complaints approved by tutor
    """

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
# PRINCIPAL DASHBOARD
# =====================================
@login_required
def principal_home(request):

    """
    Principal dashboard shows final complaint decisions
    """

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
@login_required
def notifications(request):

    complaints = Complaint.objects.filter(student=request.user)
    leaves = LeaveForm.objects.filter(student=request.user)
    outpasses = Outpass.objects.filter(student=request.user)

    return render(request, "notifications.html", {
        "complaints": complaints,
        "leaves": leaves,
        "outpasses": outpasses
    })

@login_required
def profile(request):
    return render(request, "profile.html")