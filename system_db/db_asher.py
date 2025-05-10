from django.db import models

# 5. Booking Model
# class Booking(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
#     package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='bookings')
#     booking_date = models.DateTimeField(auto_now_add=True)
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     payment_status = models.BooleanField(default=False)
#     payment_date = models.DateTimeField(null=True, blank=True)

#     def __str__(self):
#         return f"Booking {self.id} by {self.customer.user.username}"


# # 7. Wish Model
# class Wish(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='wishes')
#     package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='wishes')
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.customer.user.username}'s wish for {self.package.title}"



# # 9. Payment Model
# class Payment(models.Model):
#     booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
#     payment_method = models.CharField(max_length=50)
#     transaction_id = models.CharField(max_length=255, unique=True)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=50, default='Pending')
#     processed_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Payment for Booking {self.booking.id}"
    
    
# # 4. Customer Model
# class Customer(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
#     preferences = models.JSONField(default=dict, blank=True)  # Stores customer preferences

#     def __str__(self):
#         return self.user.username
