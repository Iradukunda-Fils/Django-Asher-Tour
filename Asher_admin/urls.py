from django.urls import path
from .views import (
    #Admin Dashboard
    AdminDashboardView,
        
    # Users URLs
    UsersView,NewUserView,EditUserView,
    
    # Booking URLs
    BookingListView,
    
    # Package URLs
    PackageAddView,PackageActiveView,PackageExpiredView,PackagePendingView,
    
    # Comments URLs
    CommentsView, 
    
    # WishList URLs
    WishListView,

)

app_name = 'Asher_admin'

urlpatterns = [
    path('', AdminDashboardView.as_view(), name='dashboard'),
]

#Users URLS

urlpatterns += [
    path('users/', UsersView.as_view(), name='users'),
    path('new_user/', NewUserView.as_view(), name='new-user'),
    path('edit_user/', EditUserView.as_view(), name='edit-user'),
    ]



#Booking URLs
urlpatterns += [
    path('bookings/', BookingListView.as_view(), name='bookings'),
    ]

#Packages URLs

urlpatterns += [
    path('package-add/', PackageAddView.as_view(), name='package-add'),
    path('package-active/', PackageActiveView.as_view(), name='package-active'),
    path('package-expired/', PackageExpiredView.as_view(), name='package-expired'),
    path('package-pending/', PackagePendingView.as_view(), name='package-pending'),
    ]

#Comments Urls

urlpatterns += [
    path('comments/', CommentsView.as_view(), name='comments'),
    ]


#WishList URLs
urlpatterns += [
    path('wish-list/', WishListView.as_view(), name='wish-list'),
    ]