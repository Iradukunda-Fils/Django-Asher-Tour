import os
import uuid
from django.db import models

def upload_to(instance, filename):
    """Custom upload path based on the tour package and company."""
    extension = filename.split('.')[-1]  # Extract the file extension (e.g., 'jpg', 'png').
    unique_name = f"{uuid.uuid4()}.{extension}"  # Generate a unique filename using UUID.
    return os.path.join(f"company_{instance.created_by.id}/package_{instance.id}/", unique_name)










from django.shortcuts import render, redirect
from .forms import TourPackageForm
from .models import TourPackage

def create_tour_package(request):
    if request.method == 'POST':
        form = TourPackageForm(request.POST, request.FILES)  # Handles submitted data and files.
        if form.is_valid():
            package = form.save(commit=False)  # Save form data, but don't commit to DB yet.
            package.created_by = request.user.tourcompany  # Assume the logged-in user is a company.
            package.save()  # Save the package to the database.

            # Handle image uploads
            image_paths = []
            for file in request.FILES.getlist('images'):  # Process each uploaded file.
                file_path = upload_to(package, file.name)  # Generate file path using `upload_to`.
                full_path = os.path.join('media', file_path)  # Complete media directory path.

                # Save file to the media directory
                with open(full_path, 'wb') as destination:
                    for chunk in file.chunks():  # Write file in chunks to handle large files.
                        destination.write(chunk)
                image_paths.append(file_path)  # Store relative path in image_paths.

            # Update the image_gallery field
            package.image_gallery = image_paths
            package.save()  # Commit changes to the database.

            return redirect('tour_package_list')  # Redirect to a list of packages.
    else:
        form = TourPackageForm()  # Render an empty form.

    return render(request, 'create_tour_package.html', {'form': form})




from django import forms
from .models import TourPackage

class TourPackageForm(forms.ModelForm):
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),  # Enables multiple file selection.
        required=False,  # Optional field.
        help_text="Upload multiple images for the tour package."  # User instructions.
    )

    class Meta:
        model = TourPackage
        fields = ['title', 'description', 'price', 'start_date', 'end_date', 'availability_status', 'images']

