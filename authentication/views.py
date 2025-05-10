from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from django.contrib import messages
from .permisions import AdminAuth
from django.urls import reverse_lazy

# Create your views here.

User = get_user_model()

class LoginView(View):
    login_url = reverse_lazy('authentication:login')
    
    def get(self, request):
        return render(request, 'auth/login.html')
    def post(self, request):
        email = request.POST.get('email')
        if email:
           messages.error(request,f"The user with email {email} does not exist")
        elif not email:
           messages.error(request,f"Prease enter your email and password")
        return redirect('authentication:login')
    
class ForgotView(AdminAuth, View):
    login_url = reverse_lazy('authentication:login')
    
    def get(self, request):
        return render(request, 'auth/forgot.html')
    def post(self, request):
        email = request.POST.get('email')
        if email:
           messages.error(request,f"The user with email {email} does not exist")
        elif not email:
           messages.error(request,f"Prease enter your email and password")
        return redirect('authentication:login')
    

    