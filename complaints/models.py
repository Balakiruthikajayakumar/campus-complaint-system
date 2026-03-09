from django.db import models
from accounts.models import User


class Complaint(models.Model):

    # =========================================================
    # COMPLAINT TYPE (ROUTING SYSTEM)
    # Determines who can see the complaint
    # =========================================================

    COMPLAINT_TYPE = (
        ('normal', 'Normal Complaint'),
        ('anonymous', 'Anonymous Complaint'),
        ('confidential', 'Confidential (Principal Only)'),
    )


    # =========================================================
    # STATUS FLOW
    # Student -> Tutor -> HOD -> Principal -> Resolved
    # =========================================================

    STATUS_CHOICES = (
        ('submitted', 'Submitted'),
        ('tutor_approved', 'Tutor Approved'),
        ('hod_approved', 'HOD Approved'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    )


    # =========================================================
    # COMPLAINT CATEGORY
    # Helps to filter complaints
    # =========================================================

    CATEGORY_CHOICES = (
        ('academic', 'Academic'),
        ('hostel', 'Hostel'),
        ('transport', 'Transport'),
        ('infrastructure', 'Infrastructure'),
        ('ragging', 'Ragging'),
        ('other', 'Other'),
    )


    # =========================================================
    # STUDENT WHO SUBMITTED COMPLAINT
    # =========================================================

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="student_complaints"
    )


    # =========================================================
    # ASSIGNED TUTOR
    # Complaint goes first to Tutor (for normal complaints)
    # =========================================================

    tutor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tutor_complaints"
    )


    # =========================================================
    # ASSIGNED HOD
    # Tutor approved complaints go to HOD
    # =========================================================

    hod = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="hod_complaints"
    )


    # =========================================================
    # COMPLAINT DETAILS
    # =========================================================

    title = models.CharField(
        max_length=200
    )

    description = models.TextField()


    # =========================================================
    # CATEGORY
    # Example: Academic / Hostel / Ragging etc
    # =========================================================

    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='academic'
    )


    # =========================================================
    # COMPLAINT TYPE
    # Normal / Anonymous / Confidential
    # =========================================================

    complaint_type = models.CharField(
        max_length=20,
        choices=COMPLAINT_TYPE,
        default='normal'
    )


    # =========================================================
    # STUDENT DETAILS (FOR FILTERING COMPLAINTS)
    # Increased length to avoid DataError
    # =========================================================

    department = models.CharField(
        max_length=50  # Increased from 20
    )

    year = models.CharField(
        max_length=20  # Increased from 5 (because "3rd Year")
    )

    section = models.CharField(
        max_length=10  # Increased slightly for safety
    )


    # =========================================================
    # IMAGE PROOF (OPTIONAL)
    # =========================================================

    image = models.ImageField(
        upload_to='complaints/',
        null=True,
        blank=True
    )


    # =========================================================
    # ANONYMOUS COMPLAINT FLAG
    # If TRUE → Student name hidden from Tutor/HOD
    # =========================================================

    is_anonymous = models.BooleanField(
        default=False
    )


    # =========================================================
    # COMPLAINT STATUS
    # =========================================================

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='submitted'
    )


    # =========================================================
    # CREATED TIME
    # =========================================================

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    # =========================================================
    # STRING REPRESENTATION
    # =========================================================

    def __str__(self):
        return self.title