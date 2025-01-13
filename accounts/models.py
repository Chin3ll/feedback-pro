from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Lecturer', 'Lecturer'),
        ('Student', 'Student'),
    ]
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=(('student', 'Student'), ('lecturer', 'Lecturer'), ('admin', 'Admin')))

    def __str__(self):
        return f"{self.user.username} - {self.role}"
