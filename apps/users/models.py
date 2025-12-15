from django.db import models
from django.contrib.auth.models import AbstractUser
from .country_choices import COUNTRY_CHOICES

# Create your models here.

class CustomUser(AbstractUser):
    # Additional fields
    date_of_birth = models.DateField(default=None, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], blank=True)
    blood_group = models.CharField(max_length=3, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')], blank=True)
    guardian_name = models.CharField(max_length=255, blank=True)
    guardian_relation = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    contact = models.CharField(max_length=15, blank=True)
    country_code = models.CharField(max_length=20, choices=COUNTRY_CHOICES, blank=True)
    
    # Track how user logged in
    login_method = models.CharField(
        max_length=20, 
        choices=[
            ('email', 'Email/Password'),
            ('google', 'Google'),
            ('facebook', 'Facebook'), 
            ('github', 'GitHub')
        ],
        default='email',
        help_text='How the user initially logged in'
    )
    
    # Track if onboarding is complete
    onboarding_complete = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class Certificate(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='certificates')
    project = models.ForeignKey('content.Project', on_delete=models.CASCADE, related_name='certificates')
    issued_at = models.DateTimeField(auto_now_add=True)
    certificate_id = models.CharField(max_length=100, unique=True, editable=False)
    
    class Meta:
        unique_together = ('user', 'project')
        ordering = ['-issued_at']

    def save(self, *args, **kwargs):
        if not self.certificate_id:
            import uuid
            from datetime import date
            
            # Use project end year if available, otherwise current year
            year = date.today().year
            if self.project and self.project.end_date:
                year = self.project.end_date.year
            
            # Format: GDA{YEAR}-{UUID_SEGMENT}
            self.certificate_id = f"GDA{year}-{str(uuid.uuid4()).split('-')[0].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Certificate: {self.user.get_full_name()} - {self.project.title}"
