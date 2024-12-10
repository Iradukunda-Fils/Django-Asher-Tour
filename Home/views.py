from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.

class HomeSiteView(TemplateView):
    template_name = 'home/index.html'
    

class AboutView(TemplateView):
    template_name = 'home/about.html'
    
    
class OurServiceView(TemplateView):
    template_name = 'home/service.html'
    
