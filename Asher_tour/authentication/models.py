# asher_admin/models.py
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator, EmailValidator
from PIL import Image  # For handling image processing
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField

class UserManager(BaseUserManager):
    """
    Custom manager for User.
    """
    def create_user(self, email, first_name, last_name, phone, country, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            country=country,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone, country, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_customer', False)

        if extra_fields.get('is_admin') is not True:
            raise ValueError(_('Superuser must have is_admin=True'))
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))

        return self.create_user(email, first_name, last_name, phone, country, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model with custom fields.
    """
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = PhoneNumberField(unique=True, null=True, blank=True)
    country = CountryField(blank_label='Select Country')
    picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    active = models.BooleanField(default=True)
    status = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)  # New field
    last_login = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'country']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # Optional: Add image resizing when saving profile pictures
        if self.picture:
            img = Image.open(self.picture.path)
            if img.height > 300 or img.width > 300:
                new_img = (300, 300)
                img.thumbnail(new_img)
                img.save(self.picture.path)
        super().save(*args, **kwargs)

