from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import AnonymousUser    

#-------------------------------- Admin Privilege ----------------------------------------#

class AdminAuth(LoginRequiredMixin):
    
    def dispatch(self, request, *args, **kwargs):
        # First check if the user is authenticated
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        
       # Check if the user is an instance of AnonymousUser (this is redundant if we already check is_authenticated)
        if isinstance(request.user, AnonymousUser):
            return super().dispatch(request, *args, **kwargs)
            

        # Check if the user has a 'company' attribute or a role
        if not request.user.is_admin:
            raise PermissionDenied("You must be associated with a admin to access this page.")

        # Check if the user has the correct role
        
        return super().dispatch(request, *args, **kwargs)
    

#-------------------------------- Staff Privilege ----------------------------------------#


class StaffAuth(LoginRequiredMixin):
    
    def dispatch(self, request, *args, **kwargs):
        # First check if the user is authenticated
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)

        # Check if the user is an instance of AnonymousUser (this is redundant if we already check is_authenticated)
        if isinstance(request.user, AnonymousUser):
            return super().dispatch(request, *args, **kwargs)
            

        # Check if the user has a 'company' attribute or a role
        if not request.is_staff:
            raise PermissionDenied("You must be associated with a company to access this page.")

        # Check if the user has the correct role
        
        return super().dispatch(request, *args, **kwargs)

#-------------------------------- Customer Privilege ----------------------------------------#

class CustomerAuth(LoginRequiredMixin):
    
    def dispatch(self, request, *args, **kwargs):
        
        if not request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        
        # Check if the user is an instance of AnonymousUser (this is redundant if we already check is_authenticated)
        if isinstance(request.user, AnonymousUser):
            return super().dispatch(request, *args, **kwargs)
            

        # Check if the user has a 'company' attribute or a role
        if not request.user.is_customer:
            raise PermissionDenied("You must be associated with a company to access this page.")

        # Check if the user has the correct role
        
        return super().dispatch(request, *args, **kwargs)


# Check if the user has a 'company' attribute (indicating association with a company)
#        if not getattr(request.user, 'company', None):
#           # Redirect to the company registration page if the user is not associated with a company
#           return redirect(reverse('company-registration'))