from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
import uuid

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)  # Set hashed password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)
        
# CREATING CUSTOM USER BECAUSE WE WANT TO USE EMAIL AS USERNAME
class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False
    )
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    # IS_STAFF & IS_SUPERUSER ARE USE TO WHILE CREATING SUPERUSER
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # EMAIL WILL BE USED AS USERNAME
    username = None
    # SETTING UP USERNAME AS EMAIL
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    def __str__(self):
        return self.email