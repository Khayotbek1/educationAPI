from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils import timezone


class User(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Administrator'),
        ('MANAGER', 'Manager'),
        ('TEACHER', 'Teacher'),
        ('STUDENT', 'Student'),
        ('PARENT', 'Parent'),
    ]
    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='STUDENT')

    phone_regex = RegexValidator(
        regex=r'^\+998\d{9}$',
        message='Telephone number must be entered in the format: +998XXXXXXXXX'
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=11, unique=True)
    additional_phone = models.CharField(validators=[phone_regex], max_length=11, blank=True, null=True)

    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)

    address = models.TextField(blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)

    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    telegram_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    telegram_username = models.CharField(max_length=100, blank=True, null=True)

    sms_notifications = models.BooleanField(default=True)
    telegram_notifications = models.BooleanField(default=False)
    email_notifications = models.BooleanField(default=False)

    is_active_user = models.BooleanField(default=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Meta:
    ordering = ['-created_at']
    verbose_name = 'Foydalanuvchi'
    verbose_name_plural = 'Foydalanuvchilar'
    indexes = [
        models.Index(fields=['role', 'is_active_user']),
        models.Index(fields=['phone_number']),
    ]
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"