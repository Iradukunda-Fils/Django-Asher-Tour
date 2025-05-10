from django import forms
from django.contrib.auth import get_user_model
# from system_db

User=get_user_model()

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'country', 'active', 'is_admin', 'is_staff', 'is_customer')

    # Custom widget for BooleanField with Bootstrap classes
    active = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Active'
    )
    is_admin = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Admin'
    )
    is_staff = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Staff'
    )
    is_customer = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Customer'
    )
    
    

#------------------------------------------------PACKAGES FORM-------------------------------------------------#

