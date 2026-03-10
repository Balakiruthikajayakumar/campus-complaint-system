from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from functools import wraps
from .forms import ComplaintForm
from .models import Complaint
from accounts.models import User


# =====================================================
# ROLE BASED ACCESS CONTROL
# Allows only specific roles to access a view
# =====================================================

def role_required(role_name):

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            # FIX: compare role safely (case insensitive)
            if request.user.role.lower() != role_name.lower():
                return HttpResponseForbidden(
                    "You are not authorized to access this page"
                )

            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


# =====================================================
# STUDENT - SUBMIT COMPLAINT
# =====================================================

@login_required
@role_required('student')
def submit_complaint(request):

    if request.method == "POST":

        form = ComplaintForm(request.POST, request.FILES)

        if form.is_valid():

            complaint = form.save(commit=False)

            # Student details
            complaint.student = request.user
            complaint.department = request.user.department
            complaint.year = request.user.year
            complaint.section = request.user.section

            # ----------------------------------------
            # ROUTING BASED ON COMPLAINT TYPE
            # ----------------------------------------

            if complaint.complaint_type == "normal":

                # Find Tutor
                tutor = User.objects.filter(
                    role="tutor",
                    department=complaint.department,
                    year=complaint.year,
                    section=complaint.section
                ).first()

                complaint.tutor = tutor

                # Find HOD
                if complaint.year == "1":

                    hod = User.objects.filter(
                        role="hod",
                        department="Science & Humanities"
                    ).first()

                else:

                    hod = User.objects.filter(
                        role="hod",
                        department=complaint.department
                    ).first()

                complaint.hod = hod


            elif complaint.complaint_type == "anonymous":

                # Skip tutor → directly to HOD
                complaint.tutor = None

                if complaint.year == "1":

                    hod = User.objects.filter(
                        role="hod",
                        department="Science & Humanities"
                    ).first()

                else:

                    hod = User.objects.filter(
                        role="hod",
                        department=complaint.department
                    ).first()

                complaint.hod = hod


            elif complaint.complaint_type == "confidential":

                # Direct to principal
                complaint.tutor = None
                complaint.hod = None


            complaint.save()

            return redirect("student_homepage")

    else:

        form = ComplaintForm()

    return render(request, "submit_complaint.html", {"form": form})


# =====================================================
# STUDENT - VIEW OWN COMPLAINTS
# =====================================================

@login_required
@role_required("student")
def my_complaints(request):

    complaints = Complaint.objects.filter(
        student=request.user
    ).order_by("-id")

    return render(request, "my_complaints.html", {"complaints": complaints})


# =====================================================
# TUTOR DASHBOARD
# Tutor sees only NORMAL complaints
# =====================================================

@login_required
@role_required("tutor")
def tutor_complaints(request):

    search = request.GET.get("search")

    complaints = Complaint.objects.filter(
        complaint_type="normal",
        status="submitted",
        department=request.user.department,
        year=request.user.year,
        section=request.user.section
    )

    if search:
        complaints = complaints.filter(title__icontains=search)

    return render(request, "tutor_complaints.html", {"complaints": complaints})


# =====================================================
# TUTOR APPROVE
# =====================================================

@login_required
@role_required("tutor")
def approve_by_tutor(request, id):

    complaint = get_object_or_404(Complaint, id=id)

    # Change status
    complaint.status = "tutor_approved"
    complaint.save()

    # Go back to complaints page
    return redirect("complaints")


# =====================================================
# TUTOR REJECT
# =====================================================

@login_required
@role_required("tutor")
def reject_by_tutor(request, id):

    complaint = get_object_or_404(Complaint, id=id)

    # Change status
    complaint.status = "rejected"
    complaint.save()

    # Go back to complaints page
    return redirect("complaints")


# =====================================================
# HOD DASHBOARD
# =====================================================

@login_required
@role_required("hod")
def hod_complaints(request):

    if request.user.department == "Science & Humanities":

        complaints = Complaint.objects.filter(
            year="1"
        ).exclude(
            complaint_type="confidential"
        )

    else:

        complaints = Complaint.objects.filter(
            department=request.user.department
        ).exclude(
            complaint_type="confidential"
        )

    return render(request, "hod_complaints.html", {"complaints": complaints})


# =====================================================
# HOD APPROVE
# =====================================================

@login_required
@role_required("hod")
def approve_by_hod(request, id):

    complaint = get_object_or_404(Complaint, id=id)

    complaint.status = "hod_approved"
    complaint.save()

    return redirect("hod_complaints")


# =====================================================
# HOD REJECT
# =====================================================

@login_required
@role_required("hod")
def reject_by_hod(request, id):

    complaint = get_object_or_404(Complaint, id=id)

    complaint.status = "rejected"
    complaint.save()

    return redirect("hod_complaints")


# =====================================================
# PRINCIPAL DASHBOARD
# Principal sees all complaints
# =====================================================

@login_required
@role_required("principal")
def principal_complaints(request):

    complaints = Complaint.objects.all()

    return render(request, "principal_complaints.html", {"complaints": complaints})


# =====================================================
# PRINCIPAL APPROVE (RESOLVE)
# =====================================================

@login_required
@role_required("principal")
def approve_by_principal(request, id):

    complaint = get_object_or_404(Complaint, id=id)

    complaint.status = "resolved"
    complaint.save()

    return redirect("principal_complaints")


# =====================================================
# PRINCIPAL REJECT
# =====================================================

@login_required
@role_required("principal")
def reject_by_principal(request, id):

    complaint = get_object_or_404(Complaint, id=id)

    complaint.status = "rejected"
    complaint.save()

    return redirect("principal_complaints")


# =====================================================
# ANONYMOUS COMPLAINT PAGE
# =====================================================

@login_required
@role_required("student")
def anonymous_complaint(request):

    if request.method == "POST":

        title = request.POST.get("title")
        description = request.POST.get("description")
        category = request.POST.get("category")
        image = request.FILES.get("image")

        Complaint.objects.create(
            student=request.user,
            title=title,
            description=description,
            category=category,
            complaint_type="anonymous",
            is_anonymous=True,
            department=request.user.department,
            year=request.user.year,
            section=request.user.section,
            image=image
        )

        return redirect("student_homepage")

    return render(request, "anonymous_complaint.html")


# =====================================================
# TRACK COMPLAINT STATUS
# Allows student / tutor / hod / principal to view status
# =====================================================

@login_required
def track_complaint(request, id):

    # Get complaint safely
    complaint = get_object_or_404(Complaint, id=id)

    # -------------------------------------------------
    # ACCESS CONTROL
    # Student can see only their complaint
    # Tutor/HOD/Principal can view complaints they manage
    # -------------------------------------------------

    if request.user.role.lower() == "student":
        if complaint.student != request.user:
            return HttpResponseForbidden(
                "You are not authorized to access this page"
            )

    # Tutor access
    elif request.user.role.lower() == "tutor":
        if complaint.tutor != request.user:
            return HttpResponseForbidden(
                "You are not authorized to access this page"
            )

    # HOD access
    elif request.user.role.lower() == "hod":
        if complaint.hod != request.user:
            return HttpResponseForbidden(
                "You are not authorized to access this page"
            )

    # Principal can see everything
    elif request.user.role.lower() == "principal":
        pass

    else:
        return HttpResponseForbidden(
            "You are not authorized to access this page"
        )

    # -------------------------------------------------
    # Render tracking page
    # -------------------------------------------------

    return render(request, "track_complaint.html", {
        "complaint": complaint
    })

@login_required
@role_required("tutor")
def complaints_page(request):

    complaints = Complaint.objects.filter(
        tutor=request.user
    ).order_by("-id")

    return render(request, "complaints.html", {
        "complaints": complaints
    })

# =====================================================
# TUTOR VIEW COMPLAINT DETAILS
# =====================================================

@login_required
@role_required("tutor")
def view_complaint(request, id):

    complaint = get_object_or_404(Complaint, id=id)

    return render(request, "view_complaint.html", {
        "complaint": complaint
    })

@login_required
def tutor_profile(request):
    return render(request, "tutor_profile.html")

#=========================================
#HOD HOME PAGE
#=========================================
@login_required
def hod_homepage(request):
    return render(request,"hod_homepage.html")

@login_required
def hod_profile(request):
    return render(request,"hod_profile.html")