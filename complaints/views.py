from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .forms import ComplaintForm
from .models import Complaint
from accounts.models import User


# =====================================================
# ROLE BASED ACCESS CONTROL
# =====================================================
def role_required(role_name):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):

            if request.user.role != role_name:
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

    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)

        if form.is_valid():

            complaint = form.save(commit=False)

            # Student Details
            complaint.student = request.user
            complaint.department = request.user.department
            complaint.year = request.user.year
            complaint.section = request.user.section

            # =========================
            # AUTO FIND TUTOR
            # =========================
            tutor = User.objects.filter(
                role='tutor',
                department=complaint.department,
                year=complaint.year,
                section=complaint.section
            ).first()

            complaint.tutor = tutor

            # =========================
            # AUTO FIND HOD
            # =========================
            if complaint.year == "1":
                hod = User.objects.filter(
                    role='hod',
                    department="Science & Humanities"
                ).first()
            else:
                hod = User.objects.filter(
                    role='hod',
                    department=complaint.department
                ).first()

            complaint.hod = hod

            complaint.save()

            return redirect('student_homepage')

    else:
        form = ComplaintForm()

    return render(
        request,
        'submit_complaint.html',
        {'form': form}
    )


# =====================================================
# STUDENT - VIEW OWN COMPLAINTS
# =====================================================
@login_required
@role_required('student')
def my_complaints(request):

    complaints = Complaint.objects.filter(
        student=request.user
    ).order_by('-id')

    return render(
        request,
        'my_complaints.html',
        {'complaints': complaints}
    )


# =====================================================
# TUTOR DASHBOARD
# =====================================================
@login_required
@role_required('tutor')
def tutor_complaints(request):

    search = request.GET.get('search')

    complaints = Complaint.objects.filter(
        status='submitted',
        department=request.user.department,
        year=request.user.year,
        section=request.user.section
    )

    if search:
        complaints = complaints.filter(
            title__icontains=search
        )

    return render(
        request,
        'tutor_complaints.html',
        {'complaints': complaints}
    )


@login_required
@role_required('tutor')
def approve_by_tutor(request, id):

    complaint = get_object_or_404(Complaint, id=id)
    complaint.status = 'tutor_approved'
    complaint.save()

    return redirect('tutor_complaints')


@login_required
@role_required('tutor')
def reject_by_tutor(request, id):

    complaint = get_object_or_404(Complaint, id=id)
    complaint.status = 'rejected'
    complaint.save()

    return redirect('tutor_complaints')


# =====================================================
# HOD DASHBOARD
# =====================================================
@login_required
@role_required('hod')
def hod_complaints(request):

    # First Year Special HOD
    if request.user.department == "Science & Humanities":
        complaints = Complaint.objects.filter(
            status='tutor_approved',
            year="1"
        )
    else:
        complaints = Complaint.objects.filter(
            status='tutor_approved',
            department=request.user.department
        )

    return render(
        request,
        'hod_complaints.html',
        {'complaints': complaints}
    )


@login_required
@role_required('hod')
def approve_by_hod(request, id):

    complaint = get_object_or_404(Complaint, id=id)
    complaint.status = 'hod_approved'
    complaint.save()

    return redirect('hod_complaints')


@login_required
@role_required('hod')
def reject_by_hod(request, id):

    complaint = get_object_or_404(Complaint, id=id)
    complaint.status = 'rejected'
    complaint.save()

    return redirect('hod_complaints')


# =====================================================
# PRINCIPAL DASHBOARD
# =====================================================
@login_required
@role_required('principal')
def principal_complaints(request):

    complaints = Complaint.objects.filter(
        status='hod_approved'
    )

    return render(
        request,
        'principal_complaints.html',
        {'complaints': complaints}
    )


@login_required
@role_required('principal')
def approve_by_principal(request, id):

    complaint = get_object_or_404(Complaint, id=id)
    complaint.status = 'resolved'
    complaint.save()

    return redirect('principal_complaints')


@login_required
@role_required('principal')
def reject_by_principal(request, id):

    complaint = get_object_or_404(Complaint, id=id)
    complaint.status = 'rejected'
    complaint.save()

    return redirect('principal_complaints')