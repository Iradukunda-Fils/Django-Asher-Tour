from django.db import models
from django.db.models import Avg
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils.timezone import now
from urllib.parse import urlencode

__all__ = [
    'Category', "TourPackage", 
    "Destination", "Itinerary", 
    "PackageMedia", "Review", 
    "PackageOffer"]

User = get_user_model()


#OPTIMIZING DISCOUNT PERCENTAGE USING MANAGER
class PackageOfferQuerySet(models.QuerySet):
    def with_related_data(self):
        # Use select_related for the tour_package ForeignKey
        return self.select_related('tour_package')


class PackageOfferManager(models.Manager):
    def get_queryset(self):
        return PackageOfferQuerySet(self.model, using=self._db).with_related_data()


class Category(models.Model):
    slug = models.SlugField(blank=True, null=True)  # Allow blank, ensure unique
    name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name']),  # Optimize category lookups by name
        ]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:  # Only generate a slug if one isn't provided
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def package(self):
        return self.packages.all()
    
    @property
    def package_count(self):
        return self.packages.all().count()

    @property
    def destination(self):
        return self.packages.destinations.count
    
    @property
    def category_url(self):
        params = {'category': self.name}
        return urlencode(params)

    
    
    

# TourPackage Model
class TourPackage(models.Model):
    slug = models.SlugField(null=True, blank=True)  # Allow blank, ensure unique
    image = models.ImageField(upload_to='package_profile/')
    title = models.CharField(max_length=255, unique=True, db_index=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='packages', db_index=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_packages', db_index=True)
    deadline = models.DateField(db_index=True)
    group_size = models.PositiveIntegerField(
        validators=[MinValueValidator(1)], 
        help_text="Minimum group size is 1"
    )
    location = CountryField(default="RW")
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
    is_active = models.BooleanField(default=True, db_index=True)
    is_published = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_active', 'is_published']),  # Optimize frequent active/published filters
            models.Index(fields=['deadline']),  # Optimize deadline-related queries
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(price__gte=0), name='price_non_negative'),
            models.CheckConstraint(check=models.Q(group_size__gte=1), name='group_size_min_one'),
        ]
        verbose_name = "Tour Package"
        verbose_name_plural = "Tour Packages"

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:  # Only generate a slug if one isn't provided
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @property
    def rating(self):
        """
        Calculate the average rating for the tour package, considering only ratings with a maximum value of 5.
        """
        # Filter reviews for this package with valid ratings (<= 5)
        avg_rating = self.reviews.filter(rating__lte=5).aggregate(Avg('rating'))['rating__avg']
        # Scale the rating to a percentage
        percentage_rating = (avg_rating / 5) * 100 if avg_rating else 0
    
        return round(percentage_rating, 2)

    
    @property
    def destination(self):
        return self.destinations.all()
    
    @property
    def schedule(self):
        return self.itineraries.all()
    
    @property
    def review(self):
        return self.reviews.all()
    

# Destination Model
class Destination(models.Model):
    image = models.ImageField(upload_to="destinations")
    tour_package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='destinations', db_index=True)
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, db_index=True)
    is_popular = models.BooleanField(default=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tour_package', 'name']),  # Optimize unique destination lookup within a package
            models.Index(fields=['is_popular']),  # Optimize popular destinations
        ]
        verbose_name = "Destination"
        verbose_name_plural = "Destinations"

    def __str__(self):
        return f"{self.name} ({self.location})"
    
    @property
    def destination_url(self):
        params = {'destination': self.name}
        return urlencode(params)
    
    # def save(self, *args, **kwargs):
    #     if self.image:
    #         # Open the uploaded image
    #         img = Image.open(self.image)
    #         output = BytesIO()

    #         # Resize the image while maintaining aspect ratio
    #         max_size = (800, 250)  # Maximum dimensions (width, height)
    #         img.thumbnail(max_size, Image.LANCZOS)

    #         # Save the resized image to the BytesIO buffer
    #         img_format = img.format or 'JPEG'
    #         img.save(output, format=img_format)
    #         output.seek(0)

    #         # Replace the original image with the resized one
    #         self.image = ContentFile(output.read(), self.image.name)

    #     # Save the instance
    #     super().save(*args, **kwargs)
    
    

# Itinerary Model
class Itinerary(models.Model):
    tour_package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='itineraries', db_index=True)
    title = models.CharField(max_length=255, db_index=True)
    day_number = models.PositiveIntegerField(db_index=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        unique_together = ('tour_package', 'day_number')  # Ensure no duplicate days for a package
        ordering = ['day_number']
        indexes = [
            models.Index(fields=['tour_package', 'day_number']),  # Optimize day-by-day itinerary queries
        ]
        verbose_name = "Itinerary"
        verbose_name_plural = "Itineraries"

    def __str__(self):
        return f"Day {self.day_number}: {self.title} - {self.tour_package.title}"

# PackageMedia Model
class PackageMedia(models.Model):
    tour_package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='media', db_index=True)
    images = models.ImageField(upload_to='package_images', help_text="List of images")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tour_package']),  # Optimize media retrieval for a package
        ]
        verbose_name = "Package Media"
        verbose_name_plural = "Package Media"

    def __str__(self):
        return f"Media for {self.tour_package.title}"

# Review Model
class Review(models.Model):
    tour_package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='reviews', db_index=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer', db_index=True)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], 
        help_text="Rating must be between 1 and 5"
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    replay = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='replies',
        help_text="Reference to another review this is a reply to"
    )

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tour_package', 'customer']),  # Optimize review lookups for a package by customer
        ]
        
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    def __str__(self):
        return f"Review by {self.customer.first_name} for {self.tour_package.title} - {self.rating} stars"
    
    @property
    def replays(self):
        return self.replies.all()
    
    @property
    def ratings(self):
        return round(self.rating * 20, 2) if self.rating else 0  # Return 0 if no reviews exist

#PACKAGE OFFER
class PackageOffer(models.Model):
    tour_package = models.OneToOneField(
        TourPackage, 
        on_delete=models.CASCADE, 
        related_name='offers', 
        db_index=True
    )
    title = models.CharField(max_length=255, unique=True, db_index=True)
    description = models.TextField(max_length=100,blank=True)
    discount_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True,
        blank=True,
        db_index=True,
        validators=[MinValueValidator(0.0)],
        help_text="Discounted price of the tour package"
    )
    start_date = models.DateTimeField(db_index=True)
    end_date = models.DateTimeField(db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    
    objects = PackageOfferManager()

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['is_active', 'start_date', 'end_date']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(discount_price__gte=0), 
                name='discount_price_non_negative'
            ),
        ]
        verbose_name = "Package Offer"
        verbose_name_plural = "Package Offers"

    def __str__(self):
        return f"Offer: {self.title} for {self.tour_package.title}"
    
    @property
    def expired(self):
        return self.end_date < now()
    
    def clean(self):
        """
        Custom validation to ensure the discount price is not greater than the tour package price.
        """
        if self.start_date is None or self.end_date is None:
            raise ValidationError("Start date and end date cannot be empty.")
        if self.discount_price and self.tour_package and self.discount_price > self.tour_package.price:
            raise ValidationError({
                'discount_price': f"The discount price ({self.discount_price}) cannot be greater than the package price ({self.tour_package.price})."
            })
        if self.start_date >= self.end_date:
            raise ValidationError({
                'end_date': f"start date {self.start_date} of offer must be less than end date {self.end_date}."
            }) 
        return super().clean()
        
        

    @property
    def discount_percentage(self):
        """
        Property to calculate the discount percentage based on the 
        original package price and the discounted price.
        """
        if self.tour_package and self.tour_package.price > 0 and self.discount_price:
            return round(
                (1 - (self.discount_price / self.tour_package.price)) * 100, 2
            )
        return 0.0
    
    @property
    def new_price(self):
        return self.tour_package.price - self.discount_price
