from django.shortcuts import render, redirect
from .models import LeaveForm
from accounts.models import User

# for My Requests page
from complaints.models import Complaint
from outpass.models import Outpass


# =====================================================
# APPLY LEAVE
# Student submits leave request
# =====================================================
def apply_leave(request):

    if request.method == "POST":

        # -----------------------------------------
        # GET DATA FROM HTML FORM
        # -----------------------------------------
        name = request.POST.get("name")
        reg_no = request.POST.get("reg_no")
        department = request.POST.get("department")
        section = request.POST.get("section")

        parent_phone = request.POST.get("parent_phone")
        confirm = request.POST.get("confirm")

        from_date = request.POST.get("from_date")
        to_date = request.POST.get("to_date")

        out_time = request.POST.get("out_time")
        in_time = request.POST.get("in_time")

        purpose = request.POST.get("purpose")


        # -----------------------------------------
        # FIND APPROVAL USERS
        # -----------------------------------------
        tutor = User.objects.filter(
            role="tutor",
            department=department,
            section=section
        ).first()

        hod = User.objects.filter(
            role="hod",
            department=department
        ).first()

        deputy = User.objects.filter(
            role="deputy_warden"
        ).first()

        warden = User.objects.filter(
            role="associate_warden"
        ).first()


        # -----------------------------------------
        # SAVE LEAVE FORM
        # -----------------------------------------
        LeaveForm.objects.create(

            student=request.user,

            name=name,
            register_number=reg_no,
            department=department,
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

        # after submit redirect
        return redirect("my_requests")

    return render(request, "apply_leave.html")


# =====================================================
# MY REQUESTS PAGE
# Shows Complaints + Leaves + Outpasses
# =====================================================
def my_requests(request):

    complaints = Complaint.objects.filter(student=request.user)

    leaves = LeaveForm.objects.filter(
        student=request.user,
        status="warden_approved"
    )


    outpasses = Outpass.objects.filter(student=request.user)

    return render(request, "my_requests.html", {
        "complaints": complaints,
        "leaves": leaves,
        "outpasses": outpasses
    })

# ==========================================
# DOWNLOAD LEAVE FILE
# ==========================================

from django.http import HttpResponse

def download_leave(request, id):

    leave = LeaveForm.objects.get(id=id)

    response = HttpResponse(content_type="text/plain")
    response["Content-Disposition"] = 'attachment; filename="leave.txt"'

    response.write("Leave Request\n")
    response.write(f"Student: {leave.name}\n")
    response.write(f"Register Number: {leave.register_number}\n")
    response.write(f"Department: {leave.department}\n")
    response.write(f"From: {leave.from_date}\n")
    response.write(f"To: {leave.to_date}\n")
    response.write(f"Reason: {leave.purpose}\n")
    response.write(f"Status: {leave.status}\n")

    return response

def leave_verification(request):
    leaves = LeaveForm.objects.filter(
        tutor=request.user,
        status="submitted"
    )
    return render(request,"leave_verification.html",{"leaves":leaves})

def tutor_approve(request,id):

    leave = LeaveForm.objects.get(id=id)

    leave.status = "tutor_approved"
    leave.save()

    return redirect("leave_verification")
def tutor_reject(request,id):

    leave = LeaveForm.objects.get(id=id)
    leave.status = "rejected"
    leave.save()

    return redirect("leave_verification")

def hod_leave_page(request):

    leaves = LeaveForm.objects.filter(
        hod=request.user,
        status="tutor_approved"
    )

    return render(request,"hod_leave.html",{"leaves":leaves})

def deputy_leave_page(request):

    leaves = LeaveForm.objects.filter(
        deputy_warden=request.user,
        status="hod_approved"
    )

    return render(request,"deputy_leave.html",{"leaves":leaves})

def warden_leave_page(request):

    leaves = LeaveForm.objects.filter(
        associate_warden=request.user,
        status="deputy_approved"
    )

    return render(request,"warden_leave.html",{"leaves":leaves})

def final_approve(request,id):

    leave = LeaveForm.objects.get(id=id)

    leave.status = "warden_approved"
    leave.save()

    return redirect("warden_leave_page")

