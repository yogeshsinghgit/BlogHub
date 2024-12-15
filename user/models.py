from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.


class CustomUserManager(BaseUserManager):
    
    def create_user(self, email, password = None, user_type='reader', **extra_fields):
        if not email:
            raise ValueError("The Email Field is Required")
        
        email = self.normalize_email(email)
        user = self.model(email = email,
                          user_type = user_type,
                          **extra_fields)
        user.set_password(password)
        user.save(using = self._db)

        return user
    

    def create_superuser(self, email, password= None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'admin')


        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

    

class CustomUser(AbstractBaseUser,PermissionsMixin):
    USER_TYPE_CHOICES = [
        ('author', "Author"),
        ('reader', "Reader"),
        ('admin', 'Admin')
    ]

    # uid = models.UUIDField(unique=True, default= uuid.uuid4)
    email = models.EmailField(unique= True)
    username = models.CharField(max_length=50, blank=True, null = True)
    user_type = models.CharField(max_length=10, choices= USER_TYPE_CHOICES, default= 'reader')
    bio = models.CharField(max_length= 255, default="No Bio Added")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} ({self.get_user_type_display()})"


