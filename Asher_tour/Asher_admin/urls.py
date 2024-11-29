from django.urls import path
from .views import Home

app_name = 'Asher_admin'

urlpatterns = [
    path('', Home.as_view(), name='dashboard'),  
]