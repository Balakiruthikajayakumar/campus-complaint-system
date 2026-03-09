from django.db import models
from accounts.models import User


class LeaveForm(models.Model):

    # =====================================================
    # STATUS OPTIONS FOR APPROVAL FLOW
    # =====================================================
    STATUS_CHOICES = (

        ('submitted', 'Submitted'),
        ('tutor_approved', 'Tutor Approved'),
        ('hod_approved', 'HOD Approved'),
        ('deputy_approved', 'Deputy Warden Approved'),
        ('warden_approved', 'Associate Warden Approved'),
        ('rejected', 'Rejected'),

    )


    # =====================================================
    # STUDENT DETAILS
    # =====================================================

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    name = models.CharField(max_length=100)

    register_number = models.CharField(max_length=20)

    department = models.CharField(max_length=50)

    section = models.CharField(max_length=10)

    parent_phone = models.CharField(max_length=15)

    confirm_with = models.CharField(max_length=20)


    # =====================================================
    # LEAVE DETAILS
    # =====================================================

    from_date = models.DateField()

    to_date = models.DateField()

    purpose = models.TextField()


    # =====================================================
    # APPROVAL FLOW USERS
    # =====================================================

    tutor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="leave_tutor"
    )

    hod = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="leave_hod"
    )

    deputy_warden = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="leave_deputy"
    )

    associate_warden = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="leave_warden"
    )


    # =====================================================
    # STATUS OF LEAVE
    # =====================================================

    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='submitted'
    )


    # =====================================================
    # CREATED DATE
    # =====================================================

    created_at = models.DateTimeField(auto_now_add=True)


    # =====================================================
    # DISPLAY NAME IN ADMIN PANEL
    # =====================================================

    def __str__(self):

        return f"{self.name} - {self.register_number}"