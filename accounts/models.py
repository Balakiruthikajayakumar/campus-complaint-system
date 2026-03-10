from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    # =====================================================
    # ROLE OPTIONS FOR USERS
    # =====================================================
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('tutor', 'Tutor'),
        ('hod', 'HOD'),
        ('deputy_warden', 'Deputy Warden'),
        ('associate_warden', 'Associate Warden'),
        ('principal', 'Principal'),
        ('admin', 'Admin'),
    )

    # =====================================================
    # DEPARTMENT OPTIONS
    # =====================================================
    DEPT_CHOICES = (
        ('cse', 'CSE'),
        ('ece', 'ECE'),
        ('eee', 'EEE'),
        ('mech', 'MECH'),
        ('it', 'IT'),
    )

    # =====================================================
    # YEAR OPTIONS
    # =====================================================
    YEAR_CHOICES = (
        ('1', '1st Year'),
        ('2', '2nd Year'),
        ('3', '3rd Year'),
        ('4', '4th Year'),
    )

    # =====================================================
    # SECTION OPTIONS
    # =====================================================
    SECTION_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    )

    # =====================================================
    # USER EXTRA FIELDS
    # =====================================================
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)

    department = models.CharField(
        max_length=50,
        choices=DEPT_CHOICES,
        null=True,
        blank=True
    )

    year = models.CharField(
        max_length=20,
        choices=YEAR_CHOICES,
        null=True,
        blank=True
    )

    section = models.CharField(
        max_length=5,
        choices=SECTION_CHOICES,
        null=True,
        blank=True
    )

    email = models.EmailField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.username