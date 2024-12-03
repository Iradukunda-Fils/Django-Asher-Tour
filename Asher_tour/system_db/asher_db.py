from django.db import models
from django.contrib.auth.models import AbstractUser

# Define the entities and attributes with constraints, data types, and relationships

# 1. User Model (Extending AbstractUser for Customer and Company Users)
class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False, max_length=255)
    is_customer = models.BooleanField(default=False)
    is_tour_company = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.username

# 2. TourCompany Model
class TourCompany(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tour_company')
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField(null=True, blank=True)
    contact_info = models.CharField(max_length=50, null=True, blank=True)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    rating = models.FloatField(default=0.0, null=True, blank=True)

    def __str__(self):
        return self.name

# 3. TourPackage Model
class TourPackage(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    availability_status = models.BooleanField(default=True)
    rating = models.FloatField(default=0.0, null=True, blank=True)
    created_by = models.ForeignKey(TourCompany, on_delete=models.CASCADE, related_name='packages')
    image_gallery = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.title

# 4. Customer Model
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    preferences = models.JSONField(default=dict, blank=True)  # Stores customer preferences

    def __str__(self):
        return self.user.username

# 5. Booking Model
class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.BooleanField(default=False)
    payment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Booking {self.id} by {self.customer.user.username}"

# 6. Comment Model
class Comment(models.Model):
    package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='comments')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    replied_by = models.ForeignKey(TourCompany, null=True, blank=True, on_delete=models.SET_NULL, related_name='replies')

    def __str__(self):
        return f"Comment by {self.customer.user.username}"

# 7. Wish Model
class Wish(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='wishes')
    package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='wishes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.user.username}'s wish for {self.package.title}"

# 8. Like Model
class Like(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='likes')
    package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f"{self.customer.user.username} liked {self.package.title}"

# 9. Payment Model
class Payment(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=255, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='Pending')
    processed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Booking {self.booking.id}"
