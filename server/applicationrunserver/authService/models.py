from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class Roles(models.TextChoices):
    USER = 'User'
    MODERATOR = 'Moderator'
    ADMIN = 'Admin'

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)  
        return user
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', Roles.ADMIN)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)


class UserServer(AbstractBaseUser):
    _id = models.AutoField(primary_key=True, editable=False)    
    name = models.CharField(max_length=30, unique=True)
    lastname = models.CharField(max_length=30, unique=True)   
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=30, unique=True)
    phone = models.CharField(max_length=30, unique=True)
    signSecret = models.TextField(null=False, blank=False, default='')
    role = models.CharField(choices=Roles.choices, default=Roles.USER, max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name', 'lastname', 'phone', 'signSecret', 'role']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    







