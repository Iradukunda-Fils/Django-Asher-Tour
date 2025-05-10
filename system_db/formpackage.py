from django import forms
from .db_package import PackageMedia, PackageOffer, Destination, Category, TourPackage, Itinerary, Review
from django.forms.widgets import ClearableFileInput

class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True

    def __init__(self, attrs=None):
        attrs = attrs or {}
        attrs['multiple'] = True
        super().__init__(attrs)


class PackageForm(forms.ModelForm):
    
    class Meta:
        model = TourPackage
        fields = "__all__"
        
class MediaPackageForm(forms.ModelForm):
    images = forms.FileField(
        widget=MultipleFileInput(attrs={'multiple': True, 'accept': 'video/*', 'id': 'video-file', 'class': 'form-control'}),
        required=True
    )
    class Meta:
        model = PackageMedia
        fields = "__all__"
        
class DestinationForms(forms.ModelForm):
    class Meta:
        model = Destination
        fields = "__all__"
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = "__all__"


class Itinerary(forms.ModelForms):
    class Meta:
        model = Itinerary
        fields = "__all__"
    
        