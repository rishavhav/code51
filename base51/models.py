from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
)

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set.")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    # Add custom fields if needed
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    # ... other fields

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    class Meta:
        swappable = "AUTH_USER_MODEL"


class SMSResponse(models.Model):
    phone_number = models.CharField(
        max_length=20, unique=True
    )  # Make phone_number field unique
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.phone_number} - {self.timestamp} - {self.seen}"


class MessageSender(models.Model):
    phone_number = models.CharField(max_length=20)
    sms_response = models.ForeignKey(
        SMSResponse, on_delete=models.SET_NULL, null=True, blank=True
    )
    date_received = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.phone_number
