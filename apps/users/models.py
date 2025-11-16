from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    # Additional fields
    date_of_birth = models.DateField(default=None, null=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    blood_group = models.CharField(max_length=3, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')])
    guardian_name = models.CharField(max_length=255)
    guardian_relation = models.CharField(max_length=100)
    address = models.TextField()
    contact = models.CharField(max_length=15)
    country_code = models.CharField(max_length=5)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
