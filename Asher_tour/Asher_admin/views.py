from django.shortcuts import render
from django.views.generic import(
    TemplateView, ListView, 
    DetailView, CreateView, 
    UpdateView, DeleteView
)

from django.urls import reverse_lazy
from .models import Booking, Package, Comments, WishList, Users

# Create your views here.

class Home(TemplateView):
    template_name = 'admin/dashboard.html'
    
    
    


# Booking Views
class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'booking/booking_list.html'
    context_object_name = 'bookings'

class BookingDetailView(LoginRequiredMixin, DetailView):
    model = Booking
    template_name = 'booking/booking_detail.html'
    context_object_name = 'booking'

class BookingCreateView(LoginRequiredMixin, CreateView):
    model = Booking
    template_name = 'booking/booking_form.html'
    fields = ['package', 'date', 'status']  # Adjust fields as needed
    success_url = reverse_lazy('booking_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BookingUpdateView(LoginRequiredMixin, UpdateView):
    model = Booking
    template_name = 'booking/booking_form.html'
    fields = ['package', 'date', 'status']
    success_url = reverse_lazy('booking_list')

class BookingDeleteView(LoginRequiredMixin, DeleteView):
    model = Booking
    template_name = 'booking/booking_confirm_delete.html'
    success_url = reverse_lazy('booking_list')

# Package Views
class PackageListView(TemplateView):
    template_name = 'package/package_list.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['packages'] = Package.objects.all()
    #     return context

class PackageDetailView(TemplateView):
    template_name = 'package/package_detail.html'

    # def get_context_data(self, pk, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['package'] = Package.objects.get(pk=pk)
    #     return context

# Comments Views
class CommentsListView(TemplateView):
    template_name = 'comments/comments_list.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['comments'] = Comments.objects.all()
    #     return context

class CommentsDetailView(TemplateView):
    template_name = 'comments/comments_detail.html'

    # def get_context_data(self, pk, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['comment'] = Comments.objects.get(pk=pk)
    #     return context

# WishList Views
class WishListView(LoginRequiredMixin, TemplateView):
    template_name = 'wishlist/wishlist.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['wishlist_items'] = WishList.objects.filter(user=self.request.user)
    #     return context

# Users Views
class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['user_profile'] = self.request.user
    #     return context

class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'users/dashboard.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['bookings'] = Booking.objects.filter(user=self.request.user)
    #     context['wishlist_items'] = WishList.objects.filter(user=self.request.user)
    #     return context