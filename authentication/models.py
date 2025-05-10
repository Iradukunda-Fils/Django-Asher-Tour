from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import EmailValidator
from PIL import Image  # For handling image processing
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField
from django.db.models.constraints import UniqueConstraint, CheckConstraint
from django.db.models import Q

class UserManager(BaseUserManager):
    """
    Custom manager for User.
    """
    def create_user(self, email, first_name, last_name, phone, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    
    def create_superuser(self, email, first_name, last_name, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)
    
        country = extra_fields.get('country', 'RW')  # Default to 'RW' if not provided
        if len(country) != 2:
            raise ValueError("Country code must be a valid 2-character ISO code.")
    
        return self.create_user(email, first_name, last_name, phone, password, **extra_fields)



    
class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model with custom fields.
    """
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = PhoneNumberField(unique=True, region="RW")
    country = CountryField(blank_label='Select Country',default='RW')
    picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)  # Renamed from 'status' to 'is_verified'
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'country']
    
    class Meta:
        ordering = ["-date_joined"]  # Newest users first
        indexes = [
            models.Index(fields=["is_staff", "active"], name="idx_is_staff_active"),
            models.Index(fields=["is_admin", "active"], name="idx_is_admin_active"),
            models.Index(fields=["is_customer", "country"], name="idx_is_customer_country"),
            models.Index(fields=["-date_joined"], name="idx_date_joined_desc"),
        ]
        constraints = [
            UniqueConstraint(fields=["email"], name="unique_email_constraint"),
            UniqueConstraint(fields=["phone"], name="unique_phone_constraint"),
            UniqueConstraint(fields=["email", "phone"], name="unique_email_phone"),
            CheckConstraint(
                check=Q(active=True) | (Q(is_staff=False) & Q(is_admin=False)),
                name="check_active_for_staff_admin"
            )
        ]

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.picture:
            try:
                img = Image.open(self.picture.path)
                if img.height > 300 or img.width > 300:
                    new_img = (300, 300)
                    img.thumbnail(new_img)
                    img.save(self.picture.path)
            except Exception as e:
                print(f"Error resizing image: {e}")
        super().save(*args, **kwargs)
