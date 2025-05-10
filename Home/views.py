from django.db.models import Prefetch
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from system_db.db_package import *
from django.views import View
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.dateparse import parse_date
from django.contrib import messages
from django.db.models.functions import Coalesce
from django.db.models import F


# Create your views here.

class HomeSiteView(ListView):
    model = Destination
    context_object_name = 'packages_destinations'
    template_name = 'home/index.html'
    
    def get_queryset(self):
        max_rating = 5.0  # Assuming the maximum rating is 5
        queryset = self.model.objects.filter(is_popular=True).select_related('tour_package').annotate(
            avg_percentage=Coalesce(Avg('tour_package__reviews__rating') / max_rating * 100, 0.0)
        )
        print(queryset.query)
        return queryset
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['package_offer'] = PackageOffer.objects.all()
        
        return context
    

class AboutView(TemplateView):
    template_name = 'home/about.html'
    
    
class OurServiceView(TemplateView):
    template_name = 'home/service.html'


class TourPackagesView(ListView):
    model = TourPackage
    template_name = 'home/tour-packages.html'
    context_object_name = 'packages'

    def get_queryset(self):
        """
        Optimize and handle advanced search filtering with validation.
        """
        queryset = TourPackage.objects.all().select_related(
            'category', 'created_by'
        ).prefetch_related('destinations')
    
        query = self.request.GET.get('q', '')
        category = self.request.GET.get('category', '')
        price_min = self.request.GET.get('price_min', '')
        price_max = self.request.GET.get('price_max', '')
        start_date = self.request.GET.get('start_date', '')
        end_date = self.request.GET.get('end_date', '')
        destination = self.request.GET.get('destination', '')
    
        # Search keyword
        if query:
            queryset = queryset.filter(
                Q(category__name__icontains=query) |
                Q(title__icontains=query) |
                Q(location__icontains=query) |
                Q(group_size__icontains=query)
            )
    
        # Filter by destination
        if destination:
            queryset = queryset.filter(destinations__name__exact=destination)
    
        # Filter by category
        if category:
            queryset = queryset.filter(category__name__exact=category)
    
        # Filter by price range
        try:
            price_min = float(price_min) if price_min else None
            price_max = float(price_max) if price_max else None
        except ValueError:
            price_min = price_max = None
    
        if price_min is not None:
            queryset = queryset.filter(price__gte=price_min)
        if price_max is not None:
            queryset = queryset.filter(price__lte=price_max)
    
        # Handle date range filtering (start_date and end_date)
        if start_date:
            start_date = parse_date(start_date)
            if start_date:
                queryset = queryset.filter(created_at__gte=start_date)
            else:
                return messages.error(self.request ,f"Invalid start date format. Use YYYY-MM-DD. try deferent to: start_date")
        if end_date:
            end_date = parse_date(end_date)
            if end_date:
                queryset = queryset.filter(created_at__lte=end_date)
            else:
                return messages.error(self.request ,"Invalid end date format. Use YYYY-MM-DD.")
            
        # Ensure start date is earlier than end date
        if start_date and end_date and start_date > end_date:
            return messages.error(self.request ,"Start date cannot be later than end date.")
        # Implement pagination to avoid large result sets
        paginator = Paginator(queryset, 6)  # Show 10 packages per page
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return page_obj
    

    def get_context_data(self, **kwargs):
        """
        Add extra context to the template, including category data.
        """
        context = super().get_context_data(**kwargs)

        # Optimize category query to prefetch related packages and destinations
        context['categories'] = Category.objects.prefetch_related(
            Prefetch('packages', queryset=TourPackage.objects.select_related('category').prefetch_related('destinations'))
        ).all()

        return context

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests with search and filtering logic, and return validation errors if necessary.
        """
        # Call the parent's get method to initialize the response
        response = super().get(request, *args, **kwargs)
        
        # Get the search query from the request
        query = request.GET.get('q', '')
        
        # If a search query is provided, pass it to the context
        if query:
            response.context_data['search_query'] = query

        return response
    
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import Prefetch

class TourPackageDetails(View):
    tour_package_model = TourPackage
    category_model = Category
    review_model = Review
    template_name = 'home/package-detail.html'
    
    def get(self, request, slug, pk):
        # Get package with prefetched reviews and their replies
        package_q = (
            self.tour_package_model.objects
            .select_related('category', 'created_by')  # Use 'created_by' instead of 'user' if applicable
            .prefetch_related(
                'destinations',
                'itineraries',
                Prefetch(
                    'reviews',
                    queryset=Review.objects.select_related('customer').prefetch_related('replies').only('rating', 'comment', 'customer', 'created_at')
                )
            )
        )


        
        package = get_object_or_404(package_q, pk=pk, slug=slug)
        print(package_q.query)
        
        # Fetch all categories (optimized)
        categories = self.category_model.objects.all()  # Avoid prefetch unless necessary
        # Filter packages with discounted price and order by the discount amount, descending
        
        highest_discount_package = PackageOffer.objects.select_related('tour_package').annotate(
            discount_amount=F('tour_package__price') - F('discount_price')
        ).filter(discount_price__isnull=False).order_by('-discount_amount').first()
        
        total_price = round(package.price * package.group_size , 2)

        # Pass the data to the template
        context = {
            'package': package,
            'categories': categories,
            'adv': highest_discount_package,
            'total_price': total_price
            
        }
        return render(request, self.template_name, context)

    def post(self, request, slug, pk):
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'message': 'Please login to submit a review'}, status=401)

        # Get the package
        package = get_object_or_404(self.tour_package_model, pk=pk, slug=slug)
        
        # Get form data
        rating = request.POST.get('rating')
        comment = request.POST.get('review_text')  # For new reviews
        reply_text = request.POST.get('reply_text')  # For replies
        review_id = request.POST.get('review_id')  # For replies
        
        rating = int(rating)
        if not 1 <= rating <= 5:
            return JsonResponse({'success': False, 'message': 'Please select a rating between 1 and 5 stars'}, status=400)
    
        # Handling review creation or reply
        if review_id:
            parent_review = get_object_or_404(self.review_model, id=review_id, tour_package=package)
            review = self.review_model.objects.create(
                tour_package=package,
                customer=request.user,
                rating=rating,
                comment=reply_text,
                replay=parent_review
            )
        else:
            review = self.review_model.objects.create(
                tour_package=package,
                customer=request.user,
                rating=rating,
                comment=comment
            )
        
        # Return success response
        response_data = {
            'success': True,
            'review': {
                'id': review.id,
                'rating': review.rating,
                'comment': review.comment,
                'customer_name': f"{review.customer.first_name} {review.customer.last_name}",
                'created_at': review.created_at.strftime("%b %d, %Y")
            }
        }
        return JsonResponse(response_data)



    
    
# class TourPackageDetails(View):
#     tour_package_model = TourPackage
#     category_model = Category
#     template_name = 'home/package-detail.html'

#     def get(self, request, slug, pk):
#         # Fetch the tour package and its category
#         from django.db.models import Prefetch

#         package_q = (
#             self.tour_package_model.objects
#             .select_related('category', 'created_by')  # Use 'created_by' instead of 'user' if applicable
#             .prefetch_related(
#                 'destinations',
#                 'itineraries',
#                 Prefetch(
#                     'reviews',
#                     queryset=Review.objects.select_related('customer').prefetch_related('replies').only('rating', 'comment', 'customer', 'created_at')
#                 )
#             )
#         )


        
#         package = get_object_or_404(package_q, pk=pk, slug=slug)
#         print(package_q.query)
        
#         # Fetch all categories (optimized)
#         categories = self.category_model.objects.all()  # Avoid prefetch unless necessary

#         # Pass the data to the template
#         context = {
#             'package': package,
#             'categories': categories,
#         }
#         return render(request, self.template_name, context)

        
        
class OfferView(View):
    template_name = 'home/package-offer.html'
    model = PackageOffer
    
    def get(self, request):
        offers = self.model.objects.filter(is_active=True).select_related('tour_package')
        context = {
            'offers': offers,
        }
        return render(request, self.template_name, context)
   


    
    
