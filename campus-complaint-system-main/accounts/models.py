from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):

    # Role Choices
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('tutor', 'Tutor'),
        ('hod', 'HOD'),
        ('principal', 'Principal'),
        ('admin', 'Admin'),
    )

    # Department Choices (Civil removed)
    DEPT_CHOICES = (
        ('cse', 'CSE'),
        ('ece', 'ECE'),
        ('eee', 'EEE'),
        ('mech', 'MECH'),
    )

    # Year Choices
    YEAR_CHOICES = (
        ('1', '1st Year'),
        ('2', '2nd Year'),
        ('3', '3rd Year'),
        ('4', '4th Year'),
    )

    # Section Choices
    SECTION_CHOICES = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    )

    # Extra Fields
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    department = models.CharField(max_length=20, choices=DEPT_CHOICES, null=True, blank=True)
    year = models.CharField(max_length=5, choices=YEAR_CHOICES, null=True, blank=True)
    section = models.CharField(max_length=5, choices=SECTION_CHOICES, null=True, blank=True)
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.username
