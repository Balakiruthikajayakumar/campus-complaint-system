from django.db import models
from accounts.models import User


class Complaint(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    image = models.ImageField(
        upload_to='complaints/',
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=30,
        default='submitted'
    )

    STATUS_CHOICES = (
        ('submitted', 'Submitted'),
        ('tutor_approved', 'Tutor Approved'),
        ('hod_approved', 'HOD Approved'),
        ('resolved', 'Resolved'),
        ('rejected', 'Rejected'),
    )

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="student_complaints"
    )

    # NEW ⭐
    tutor = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tutor_complaints"
    )

    hod = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="hod_complaints"
    )

    title = models.CharField(max_length=200)
    description = models.TextField()

    department = models.CharField(max_length=20)
    year = models.CharField(max_length=5)
    section = models.CharField(max_length=5)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='submitted'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title