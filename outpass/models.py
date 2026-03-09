from django.db import models
from accounts.models import User


class Outpass(models.Model):

    STATUS_CHOICES = [
        ('pending','Pending'),
        ('approved','Approved'),
        ('rejected','Rejected')
    ]

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    from_date = models.DateField()
    to_date = models.DateField()
    out_time = models.TimeField(null=True, blank=True)
    in_time = models.TimeField(null=True, blank=True)

    reason = models.TextField()

    parent_phone = models.CharField(max_length=15)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student.username