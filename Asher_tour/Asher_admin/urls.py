from django.urls import path
from .views import Home
from django.urls import path
from .views import (
    # Booking URLs
    BookingListView, 
    BookingDetailView, 
    BookingCreateView, 
    BookingUpdateView, 
    BookingDeleteView,
    
    # Package URLs
    PackageListView, 
    PackageDetailView,
    
    # Comments URLs
    CommentsListView, 
    CommentsDetailView,
    
    # WishList URLs
    WishListView,
    
    # Users URLs
    UserProfileView, 
    UserDashboardView
)

app_name = 'Asher_admin'

urlpatterns = [
    path('', Home.as_view(), name='dashboard'),  
]



app_name = 'asher_admin'  # This creates a namespace for the URLs

urlpatterns = [
    # Booking URLs
    path('bookings/', BookingListView.as_view(), name='booking_list'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name='booking_detail'),
    path('bookings/create/', BookingCreateView.as_view(), name='booking_create'),
    path('bookings/<int:pk>/update/', BookingUpdateView.as_view(), name='booking_update'),
    path('bookings/<int:pk>/delete/', BookingDeleteView.as_view(), name='booking_delete'),
    
    # Package URLs
    path('packages/', PackageListView.as_view(), name='package_list'),
    path('packages/<int:pk>/', PackageDetailView.as_view(), name='package_detail'),
    
    # Comments URLs
    path('comments/', CommentsListView.as_view(), name='comments_list'),
    path('comments/<int:pk>/', CommentsDetailView.as_view(), name='comments_detail'),
    
    # WishList URLs
    path('wishlist/', WishListView.as_view(), name='wishlist'),
    
    # Users URLs
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('dashboard/', UserDashboardView.as_view(), name='user_dashboard'),
]