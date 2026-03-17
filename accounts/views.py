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
# LOGIN USER
# =====================================
def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        print("DEBUG:", username, password)

        user = authenticate(request, username=username, password=password)

        # ✅ CHECK USER FIRST
        if user is None:
            print("❌ LOGIN FAILED")
            messages.error(request, "Invalid Username or Password")
            return render(request, 'login.html')

        # ✅ LOGIN SUCCESS
        login(request, user)

        # ⚠️ EXTRA SAFETY (VERY IMPORTANT)
        if not hasattr(user, 'role') or user.role is None:
            print("❌ ROLE NOT FOUND")
            messages.error(request, "User role not set")
            return redirect('login')

        role = user.role.lower()
        print("ROLE:", role)

        # ✅ REDIRECT BASED ON ROLE
        if role == 'student':
            return redirect('student_homepage')

        elif role == 'tutor':
            return redirect('tutor_homepage')

        elif role == 'hod':
            return redirect('hod_homepage')

        elif role == 'principal':
            return redirect('principal_homepage')

        elif role == 'deputy_warden':
            return redirect('deputy_warden_homepage')

        elif role == 'associate_warden':
            return redirect('associate_warden_homepage')

        else:
            return redirect('/admin/')

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


# =====================================
# DEPUTY WARDEN DASHBOARD
# =====================================
@login_required
def deputy_warden_home(request):
    pending = LeaveForm.objects.filter(
        deputy_warden=request.user,
        status="hod_approved"
    ).count()

    approved = LeaveForm.objects.filter(
        deputy_warden=request.user,
        status="deputy_approved"
    ).count()

    context = {
        "pending_count": pending,
        "approved_count": approved,
    }

    return render(request, "deputy_warden_homepage.html", context)


# =====================================
# ASSOCIATE WARDEN DASHBOARD
# =====================================
@login_required
def associate_warden_home(request):
    pending = LeaveForm.objects.filter(
        associate_warden=request.user,
        status="deputy_approved"
    ).count()

    approved = LeaveForm.objects.filter(
        associate_warden=request.user,
        status="warden_approved"
    ).count()

    context = {
        "pending_count": pending,
        "approved_count": approved,
    }

    return render(request, "associate_warden_homepage.html", context)
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
#==============================
#===principal commplaints======
#==============================

from django.shortcuts import get_object_or_404

@login_required
def principal_complaints(request):

    complaints = Complaint.objects.all()

    return render(request, "principal_complaints.html", {
        "complaints": complaints
    })


def approve_complaint(request, id):
    c = Complaint.objects.get(id=id)
    c.status = "Approved"
    c.save()
    return redirect('principal_college_complaints')


def reject_complaint(request, id):
    c = Complaint.objects.get(id=id)
    c.status = "Rejected"
    c.save()
    return redirect('principal_college_complaints')



def principal_college_complaints(request):

    status = request.GET.get('status')

    if status and status != "All":
        complaints = Complaint.objects.filter(category="college", status=status)
    else:
        complaints = Complaint.objects.filter(category="college")

    return render(request, "principal_complaints.html", {
        "complaints": complaints
    })


@login_required
def principal_hostel_complaints(request):
    complaints = Complaint.objects.filter(category="hostel")
    return render(request, "principal_hostel.html", {"complaints": complaints})


@login_required
def principal_anonymous_complaints(request):
    complaints = Complaint.objects.filter(category="anonymous")
    return render(request, "principal_anonymous.html", {"complaints": complaints})
def deputy_hostel_complaints(request):
    return render(request, "deputy_hostel_complaints.html")