from django.conf import settings
from django.shortcuts import render

class CustomErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404 and settings.DEBUG:
            return render(request, '404.html', status=404)
        elif response.status_code == 500 and settings.DEBUG:
            return render(request, '500.html', status=500)
        return response
