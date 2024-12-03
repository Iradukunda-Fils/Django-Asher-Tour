from django.shortcuts import render
from django.views.generic import(
    TemplateView, ListView, 
    DetailView, CreateView, 
    UpdateView, DeleteView
)
from django.urls import reverse_lazy

# Create your views here.




class AdminDashboardView(TemplateView):
    template_name = 'admin/dashboard.html'
    
    
    


# Booking Views
class BookingListView(TemplateView):
    template_name = 'admin/booking.html'

# class BookingDetailView(LoginRequiredMixin, DetailView):
#     model = Booking
#     template_name = 'booking/booking_detail.html'
#     context_object_name = 'booking'

# class BookingCreateView(LoginRequiredMixin, CreateView):
#     model = Booking
#     template_name = 'booking/booking_form.html'
#     fields = ['package', 'date', 'status']  # Adjust fields as needed
#     success_url = reverse_lazy('booking_list')

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super().form_valid(form)

# class BookingUpdateView(LoginRequiredMixin, UpdateView):
#     model = Booking
#     template_name = 'booking/booking_form.html'
#     fields = ['package', 'date', 'status']
#     success_url = reverse_lazy('booking_list')

# class BookingDeleteView(LoginRequiredMixin, DeleteView):
#     model = Booking
#     template_name = 'booking/booking_confirm_delete.html'
#     success_url = reverse_lazy('booking_list')

# Package Views
class PackageAddView(TemplateView):
    template_name = 'admin/package/add-package.html'
    
class PackageActiveView(TemplateView):
    template_name = 'admin/package/package-active.html'
    
class PackageExpiredView(TemplateView):
    template_name = 'admin/package/package-expired.html'
    
class PackagePendingView(TemplateView):
    template_name = 'admin/package/package-expired.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['packages'] = Package.objects.all()
    #     return context

# class PackageDetailView(TemplateView):
#     template_name = 'package/package_detail.html'

    # def get_context_data(self, pk, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['package'] = Package.objects.get(pk=pk)
    #     return context

# # Comments Views
class CommentsView(TemplateView):
    template_name = 'admin/comments.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['comments'] = Comments.objects.all()
    #     return context

# class CommentsDetailView(TemplateView):
#     template_name = 'comments/comments_detail.html'

    # def get_context_data(self, pk, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['comment'] = Comments.objects.get(pk=pk)
    #     return context

# WishList Views
class WishListView(TemplateView):
    template_name = 'admin/wishlist.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['wishlist_items'] = WishList.objects.filter(user=self.request.user)
    #     return context

# Users Views
class UsersView(TemplateView):
    template_name = 'admin/users.html'
    
class NewUserView(TemplateView):
    template_name = 'admin/users/new-user.html'
    
    
class EditUserView(TemplateView):
    template_name = 'admin/users/user-edit.html'

# class UserProfileView(TemplateView):
#     template_name = 'users/profile.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['user_profile'] = self.request.user
    #     return context

# class UserDashboardView(TemplateView):
#     template_name = 'users/dashboard.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['bookings'] = Booking.objects.filter(user=self.request.user)
    #     context['wishlist_items'] = WishList.objects.filter(user=self.request.user)
    #     return context