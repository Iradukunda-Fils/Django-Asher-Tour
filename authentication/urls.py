from django.urls import path
from .views import LoginView, ForgotView

app_name = 'authentication'

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('forgot-password/', ForgotView.as_view(), name='forgot'),
]


