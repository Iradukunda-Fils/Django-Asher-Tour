from django.urls import path
from .views import *

app_name = 'Home'

urlpatterns = [
    path('', HomeSiteView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('service/', OurServiceView.as_view(), name='service'),
    path('tour-packages/', TourPackagesView.as_view(), name='tour-packages'),
    path('tour-package/details/<slug:slug>-<int:pk>', TourPackageDetails.as_view(), name='package-detail'),
    path('package-offers/', OfferView.as_view(), name='package-offers'),
]

