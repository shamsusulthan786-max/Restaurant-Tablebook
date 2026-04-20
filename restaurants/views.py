from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Restaurant, Review
from .forms import ReviewForm

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurants/restaurant_list.html', {'restaurants': restaurants})

def restaurant_detail(request, pk):
    restaurant = get_object_or_404(
        Restaurant.objects.prefetch_related('tables', 'categories__items', 'reviews'),
        pk=pk
    )
    return render(request, 'restaurants/restaurant_detail.html', {'restaurant': restaurant})

@login_required
def add_review(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.restaurant = restaurant
            review.save()
            messages.success(request, "Your review has been added successfully!")
            return redirect('restaurants:restaurant_detail', pk=restaurant.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ReviewForm()
    return render(request, 'restaurants/add_review.html', {'form': form, 'restaurant': restaurant})