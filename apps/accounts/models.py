from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User model with role-based access control."""
    
    class Role(models.TextChoices):
        STUDENT = 'STUDENT', 'Student'
        FACULTY = 'FACULTY', 'Faculty/Evaluator'
        EMPLOYER = 'EMPLOYER', 'Employer/Guest'
        ADMIN = 'ADMIN', 'Administrator'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT
    )
    student_id = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        unique=True
    )
    department = models.CharField(
        max_length=100,
        default='BSIT'
    )
    bio = models.TextField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"

    def is_student(self):
        return self.role == self.Role.STUDENT

    def is_faculty(self):
        return self.role == self.Role.FACULTY

    def is_employer(self):
        return self.role == self.Role.EMPLOYER

    def is_admin_user(self):
        return self.role == self.Role.ADMIN


class UserProfile(models.Model):
    """Extended user profile for additional metadata."""
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    specialization = models.CharField(max_length=255, blank=True, null=True)
    institution = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    profile_views = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Profile of {self.user.get_full_name()}"
