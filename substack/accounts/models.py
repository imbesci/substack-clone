from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.

class SubstackUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None):
        if not email:
            raise ValueError("Users must register with an email address.")
        if not username:
            raise ValueError("Users must create a username.")
        if not first_name:
            raise ValueError("User must enter a first name")
        if not last_name:
            raise ValueError("User must enter a last name")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            password = password,
            )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class SubstackUser(AbstractBaseUser):
    
    first_name     = models.CharField(verbose_name='first name', max_length=40)
    last_name      = models.CharField(verbose_name='last name', max_length=40)
    email          = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username       = models.CharField(max_length=30, unique=True)
    date_joined    = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login     = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin       = models.BooleanField(default = False)
    is_active      = models.BooleanField(default = True)
    is_staff       = models.BooleanField(default = False)
    is_superuser   = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username',]

    objects = SubstackUserManager()

    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    

