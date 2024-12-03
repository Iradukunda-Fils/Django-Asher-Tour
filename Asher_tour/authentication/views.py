from django.shortcuts import render
from django.views import View

# Create your views here.

class LoginView(View):
    def get(self, request):
        return render(request, 'auth/login.html')
    
class ForgotView(View):
    def get(self, request):
        return render(request, 'auth/forgot.html')
    