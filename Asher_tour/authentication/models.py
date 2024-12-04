# asher_admin/models.py
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

        return self.create_user(email, first_name, last_name, phone, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model with custom fields.
    """
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = PhoneNumberField(unique=True, null=True, blank=True)
    country = CountryField(blank_label='Select Country',null=True)
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
    
    class Meta:
        ordering = ["-date_joined"]  # Newest users first
        indexes = [
            # Composite index for frequent filtering by roles and activity
            models.Index(fields=["is_staff", "active"], name="idx_is_staff_active"),
            models.Index(fields=["is_admin", "active"], name="idx_is_admin_active"),
            models.Index(fields=["is_customer", "country"], name="idx_is_customer_country"),
            # Index for frequent ordering by date joined
            models.Index(fields=["-date_joined"], name="idx_date_joined_desc"),
        ]
        constraints = [
            # Unique constraint to ensure email uniqueness
            UniqueConstraint(fields=["email"], name="unique_email_constraint"),
            # Unique constraint to ensure phone number uniqueness, but only when phone is not null
            UniqueConstraint(fields=["phone"], name="unique_phone_constraint"),
            # Unique combinations for ensuring no duplication
            UniqueConstraint(fields=["email", "phone"], name="unique_email_phone"),
            UniqueConstraint(fields=["first_name", "last_name", "country"], name="unique_name_country"),
            UniqueConstraint(fields=["email", "country"], name="unique_email_country"),
            UniqueConstraint(fields=["phone", "country"], name="unique_phone_country"),
            # Prevent inactive users from being marked as staff or admin
            CheckConstraint(
                check=Q(active=True) | (Q(is_staff=False) & Q(is_admin=False)),
                name="check_active_for_staff_admin"
            )
        ]

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
        
    

