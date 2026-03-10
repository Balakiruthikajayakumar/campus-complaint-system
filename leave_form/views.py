from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from .models import LeaveForm
from accounts.models import User

from complaints.models import Complaint
from outpass.models import Outpass


# =====================================================
# APPLY LEAVE (STUDENT)
# =====================================================


def apply_leave(request):

    if request.method == "POST":

        # =========================
        # GET DATA FROM FORM
        # =========================

        name = request.POST.get("name")
        reg_no = request.POST.get("reg_no")
        department = request.POST.get("department")
        year = request.POST.get("year")
        section = request.POST.get("section")

        parent_phone = request.POST.get("parent_phone")
        confirm = request.POST.get("confirm")

        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")

        purpose = request.POST.get("purpose")


        # =========================
        # FIND TUTOR (SECTION WISE)
        # =========================

        tutor = User.objects.filter(
            role="tutor",
            department=department.lower(),
            year=year,
            section=section
        ).first()


        # =========================
        # FIND HOD (DEPARTMENT WISE)
        # =========================

        hod = User.objects.filter(
            role="hod",
            department=department.lower()
        ).first()


        # =========================
        # FIND DEPUTY WARDEN
        # =========================

        deputy = User.objects.filter(
            role="deputy_warden"
        ).first()


        # =========================
        # FIND ASSOCIATE WARDEN
        # =========================

        warden = User.objects.filter(
            role="associate_warden"
        ).first()


        # =========================
        # SAVE LEAVE REQUEST
        # =========================

        LeaveForm.objects.create(

            student=request.user,
            name=name,
            register_number=reg_no,

            department=department,
            year=year,
            section=section,

            parent_phone=parent_phone,
            confirm_with=confirm,

            from_date=from_date,
            to_date=to_date,

            purpose=purpose,

            tutor=tutor,
            hod=hod,
            deputy_warden=deputy,
            associate_warden=warden,

            status="submitted"
        )


        # =========================
        # AFTER SUBMIT REDIRECT
        # =========================

        return redirect("my_requests")


    return render(request, "apply_leave.html")

# =====================================================
# STUDENT MY REQUESTS PAGE
# =====================================================

def my_requests(request):

    # complaints of this student
    complaints = Complaint.objects.filter(student=request.user)

    # ALL leaves of this student
    leaves = LeaveForm.objects.filter(student=request.user)

    # outpasses
    outpasses = Outpass.objects.filter(student=request.user)

    return render(request, "my_requests.html", {
        "complaints": complaints,
        "leaves": leaves,
        "outpasses": outpasses
    })

# =====================================================
# DOWNLOAD LEAVE FILE
# =====================================================

def download_leave(request, id):

    leave = LeaveForm.objects.get(id=id)

    response = HttpResponse(content_type="text/plain")

    response['Content-Disposition'] = 'attachment; filename="leave.txt"'

    response.write(f"Student: {leave.name}\n")
    response.write(f"Register Number: {leave.register_number}\n")
    response.write(f"Department: {leave.department}\n")
    response.write(f"From: {leave.from_date}\n")
    response.write(f"To: {leave.to_date}\n")
    response.write(f"Reason: {leave.purpose}\n")

    return response


# =====================================================
# TUTOR PAGE
# =====================================================

def leave_verification(request):

    # show all leaves assigned to this tutor
    leaves = LeaveForm.objects.filter(
        tutor=request.user
    )

    return render(request, "leave_verification.html", {
        "leaves": leaves
    })


def tutor_approve(request, id):

    leave = get_object_or_404(LeaveForm, id=id)

    leave.status = "tutor_approved"
    leave.save()

    return redirect("leave_verification")


def tutor_reject(request, id):

    leave = get_object_or_404(LeaveForm, id=id)

    leave.status = "rejected"
    leave.save()

    return redirect("leave_verification")


# =====================================================
# HOD PAGE
# =====================================================

def hod_leave_page(request):

    leaves = LeaveForm.objects.filter(
        hod=request.user,
        status="tutor_approved"
    )

    return render(request, "hod_leave.html", {"leaves": leaves})


def hod_approve(request, id):

    leave = get_object_or_404(LeaveForm, id=id)

    leave.status = "hod_approved"
    leave.save()

    return redirect("hod_leave_page")


# =====================================================
# DEPUTY WARDEN PAGE
# =====================================================

def deputy_leave_page(request):

    leaves = LeaveForm.objects.filter(
        deputy_warden=request.user,
        status="hod_approved"
    )

    return render(request, "deputy_leave.html", {"leaves": leaves})


def deputy_approve(request, id):

    leave = get_object_or_404(LeaveForm, id=id)

    leave.status = "deputy_approved"
    leave.save()

    return redirect("deputy_leave_page")


# =====================================================
# ASSOCIATE WARDEN PAGE
# =====================================================

def warden_leave_page(request):

    leaves = LeaveForm.objects.filter(
        associate_warden=request.user,
        status="deputy_approved"
    )

    return render(request, "warden_leave.html", {"leaves": leaves})


def final_approve(request, id):

    leave = get_object_or_404(LeaveForm, id=id)

    leave.status = "warden_approved"
    leave.save()

    return redirect("warden_leave_page")