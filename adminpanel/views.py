from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Models
from restaurants.models import Restaurant, Table, MenuCategory, MenuItem, Review
from bookings.models import Booking

# Forms
from .forms import (
    AdminUserCreateForm,
    RestaurantForm,
    TableForm,
    MenuCategoryForm,
    MenuItemForm,
    ReviewForm,
    BookingForm,
)
# Create your views here.


def staff_required(view_func):
    return user_passes_test(lambda u: u.is_staff)(view_func)

@staff_required
def admin_dashboard(request):
    bookings = Booking.objects.all().order_by('-date', '-start_time')
    return render(request, 'adminpanel/admin_dashboard.html', {'bookings': bookings})

@staff_required
def admin_cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.status = 'cancelled'
    booking.save()
    messages.info(request, f"Booking #{booking.id} cancelled by admin.")
    return redirect('adminpanel:admin_dashboard')

@staff_required
def admin_confirm_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.status = 'confirmed'
    booking.save()
    messages.success(request, f"Booking #{booking.id} confirmed by admin.")
    return redirect('adminpanel:admin_dashboard')

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('adminpanel:admin_dashboard')
        else:
            messages.error(request, "Invalid credentials or not an admin.")
    return render(request, 'adminpanel/admin_login.html')

def admin_logout(request):
    logout(request)
    return redirect('adminpanel:admin_login')

@staff_required
def create_user(request):
    if request.method == 'POST':
        form = AdminUserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # hash password
            user.save()
            messages.success(request, "User profile created successfully!")
            return redirect('adminpanel:admin_dashboard')
    else:
        form = AdminUserCreateForm()
    return render(request, 'adminpanel/create_user.html', {'form': form})


# --- Bookings ---
@staff_required
def booking_list(request):
    bookings = Booking.objects.all()
    return render(request, 'adminpanel/booking_list.html', {'bookings': bookings})

@staff_required
def booking_edit(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            messages.success(request, "Booking updated successfully!")
            return redirect('adminpanel:booking_list')
    else:
        form = BookingForm(instance=booking)
    return render(request, 'adminpanel/booking_form.html', {'form': form, 'form_title': 'Edit Booking'})

@staff_required
def booking_delete(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, "Booking deleted successfully!")
        return redirect('adminpanel:booking_list')
    return render(request, 'adminpanel/booking_confirm_delete.html', {'booking': booking})



# --- Restaurants ---
@staff_required
def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'adminpanel/restaurant_list.html', {'restaurants': restaurants})

@staff_required
def restaurant_create(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES)  # include request.FILES for image upload
        if form.is_valid():
            form.save()
            messages.success(request, "Restaurant added successfully!")
            return redirect('adminpanel:restaurant_list')
    else:
        form = RestaurantForm()
    return render(request, 'adminpanel/restaurant_form.html', {'form': form, 'form_title': 'Add Restaurant'})

@staff_required
def restaurant_edit(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
        if form.is_valid():
            form.save()
            messages.success(request, "Restaurant updated successfully!")
            return redirect('adminpanel:restaurant_list')
    else:
        form = RestaurantForm(instance=restaurant)
    return render(request, 'adminpanel/restaurant_form.html', {'form': form, 'form_title': 'Edit Restaurant'})

@staff_required
def restaurant_delete(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if request.method == 'POST':
        restaurant.delete()
        messages.success(request, "Restaurant deleted successfully!")
        return redirect('adminpanel:restaurant_list')
    return render(request, 'adminpanel/restaurant_confirm_delete.html', {'restaurant': restaurant})

# --- Tables ---
@staff_required
def table_list(request):
    tables = Table.objects.all()
    return render(request, 'adminpanel/table_list.html', {'tables': tables})

@staff_required
def table_create(request):
    if request.method == 'POST':
        form = TableForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Table added successfully!")
            return redirect('adminpanel:table_list')
    else:
        form = TableForm()
    return render(request, 'adminpanel/table_form.html', {'form': form, 'form_title': 'Add Table'})

@staff_required
def table_edit(request, pk):
    table = get_object_or_404(Table, pk=pk)
    if request.method == 'POST':
        form = TableForm(request.POST, instance=table)
        if form.is_valid():
            form.save()
            messages.success(request, "Table updated successfully!")
            return redirect('adminpanel:table_list')
    else:
        form = TableForm(instance=table)
    return render(request, 'adminpanel/table_form.html', {'form': form, 'form_title': 'Edit Table'})

@staff_required
def table_delete(request, pk):
    table = get_object_or_404(Table, pk=pk)
    if request.method == 'POST':
        table.delete()
        messages.success(request, "Table deleted successfully!")
        return redirect('adminpanel:table_list')
    return render(request, 'adminpanel/table_confirm_delete.html', {'table': table})




# --- Menu Categories ---
@staff_required
def category_list(request):
    categories = MenuCategory.objects.all()
    return render(request, 'adminpanel/category_list.html', {'categories': categories})

@staff_required
def category_create(request):
    if request.method == 'POST':
        form = MenuCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully!")
            return redirect('adminpanel:category_list')
    else:
        form = MenuCategoryForm()
    return render(request, 'adminpanel/category_form.html', {'form': form, 'form_title': 'Add Category'})

@staff_required
def category_edit(request, pk):
    category = get_object_or_404(MenuCategory, pk=pk)
    if request.method == 'POST':
        form = MenuCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully!")
            return redirect('adminpanel:category_list')
    else:
        form = MenuCategoryForm(instance=category)
    return render(request, 'adminpanel/category_form.html', {'form': form, 'form_title': 'Edit Category'})

@staff_required
def category_delete(request, pk):
    category = get_object_or_404(MenuCategory, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, "Category deleted successfully!")
        return redirect('adminpanel:category_list')
    return render(request, 'adminpanel/category_confirm_delete.html', {'category': category})




# --- Menu Items ---
@staff_required
def item_list(request):
    items = MenuItem.objects.all()
    return render(request, 'adminpanel/item_list.html', {'items': items})

@staff_required
def item_create(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Item added successfully!")
            return redirect('adminpanel:item_list')
    else:
        form = MenuItemForm()
    return render(request, 'adminpanel/item_form.html', {'form': form, 'form_title': 'Add Item'})

@staff_required
def item_edit(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Item updated successfully!")
            return redirect('adminpanel:item_list')
    else:
        form = MenuItemForm(instance=item)
    return render(request, 'adminpanel/item_form.html', {'form': form, 'form_title': 'Edit Item'})

@staff_required
def item_delete(request, pk):
    item = get_object_or_404(MenuItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        messages.success(request, "Item deleted successfully!")
        return redirect('adminpanel:item_list')
    return render(request, 'adminpanel/item_confirm_delete.html', {'item': item})



# --- Reviews ---
@staff_required
def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'adminpanel/review_list.html', {'reviews': reviews})

@staff_required
def review_edit(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Review updated successfully!")
            return redirect('adminpanel:review_list')
    else:
        form = ReviewForm(instance=review)
    return render(request, 'adminpanel/review_form.html', {'form': form, 'form_title': 'Edit Review'})

@staff_required
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review.delete()
        messages.success(request, "Review deleted successfully!")
        return redirect('adminpanel:review_list')
    return render(request, 'adminpanel/review_confirm_delete.html', {'review': review})


    