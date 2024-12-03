from django.urls import path
from .views import HomeSiteView, AboutView, OurServiceView

app_name = 'Home'

urlpatterns = [
    path('', HomeSiteView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('service/', OurServiceView.as_view(), name='service'),
]

