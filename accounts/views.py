from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.contrib import messages
from django.http import JsonResponse
from django.db import transaction
from .models import Reservation, Bill, Order, Meal, OrderItem
from .forms import ReservationForm, OrderForm, OrderItemForm, MealForm
from decimal import Decimal

User = get_user_model()

def is_staff(user):
    return user.is_staff

def home(request):
    return render(request, 'home.html')

@login_required
@user_passes_test(is_staff)
def staff_dashboard(request):
    return render(request, 'accounts/staff_dashboard.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        age = request.POST.get('age')
        phone_number = request.POST.get('phone_number', '')
        address = request.POST.get('address', '')

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists")
            else:
                user = User.objects.create_user(
                    username=username, 
                    email=email, 
                    password=password1,
                    first_name=first_name,
                    last_name=last_name
                )
                user.age = age
                user.phone_number = phone_number
                user.address = address
                user.save()

                customer_group, created = Group.objects.get_or_create(name='Customer')
                user.groups.add(customer_group)

                login(request, user)
                messages.success(request, "Registration successful. You've been added to the Customer group.")
                return redirect('home')
        else:
            messages.error(request, "Passwords don't match")
    
    return render(request, 'accounts/register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('login_success')
            else:
                messages.error(request, "Your account has been deactivated.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'accounts/login.html')

def login_success(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('staff_dashboard')
        else:
            messages.success(request, "You have successfully logged in.")
            return render(request, 'accounts/login_success.html')
    else:
        messages.error(request, "You must be logged in to access this page.")
        return redirect('login')

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, "You have been successfully logged out.")
    return redirect('home')

@login_required
def order_meal(request):
    meals = Meal.objects.all().order_by('category', 'name')
    meal_categories = {}
    for meal in meals:
        if meal.category not in meal_categories:
            meal_categories[meal.category] = []
        meal_categories[meal.category].append(meal)

    if request.method == 'POST':
        order = Order.objects.create(customer=request.user, total_price=Decimal('0'))
        total_price = Decimal('0')
        
        for meal in meals:
            quantity = int(request.POST.get(f'quantity_{meal.id}', 0))
            if quantity > 0:
                OrderItem.objects.create(order=order, meal=meal, quantity=quantity)
                total_price += meal.price * quantity
        
        order.total_price = total_price
        order.save()
        
        bill = Bill.objects.create(customer=request.user, order=order, amount=total_price)
        
        messages.success(request, f"Order placed successfully. Bill ID: {bill.id}")
        return redirect('bill_detail', bill_id=bill.id)

    context = {
        'meal_categories': meal_categories,
    }
    return render(request, 'accounts/order_meal.html', context)

@login_required
def reserve_table(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.customer = request.user
            reservation.table_number = Reservation.objects.count() + 1
            reservation.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Your table has been reserved successfully!',
                'reservation_details': {
                    'date': reservation.date.strftime('%Y-%m-%d'),
                    'time': reservation.time.strftime('%H:%M'),
                    'guests': reservation.number_of_guests,
                    'table': reservation.table_number
                }
            })
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        form = ReservationForm()
    return render(request, 'accounts/reserve_table.html', {'form': form})

@login_required
def reservation_list(request):
    reservations = Reservation.objects.filter(customer=request.user)
    return render(request, 'accounts/reservation_list.html', {'reservations': reservations})

@login_required
def update_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, customer=request.user)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reservation updated successfully.')
            return redirect('reservation_list')
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'accounts/update_reservation.html', {'form': form, 'reservation': reservation})

@login_required
def delete_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk, customer=request.user)
    if request.method == 'POST':
        reservation.delete()
        messages.success(request, 'Reservation deleted successfully.')
        return redirect('reservation_list')
    return render(request, 'accounts/delete_reservation.html', {'reservation': reservation})

@login_required
def bill_list(request):
    bills = Bill.objects.filter(customer=request.user)
    return render(request, 'accounts/bill_list.html', {'bills': bills})

@login_required
def bill_detail(request, bill_id):
    try:
        bill = Bill.objects.get(id=bill_id, customer=request.user)
        return render(request, 'accounts/bill_detail.html', {'bill': bill})
    except Bill.DoesNotExist:
        messages.error(request, f"Bill with ID {bill_id} not found.")
        return redirect('home')

@login_required
@user_passes_test(is_staff)
def meal_list(request):
    meals = Meal.objects.all()
    return render(request, 'accounts/meal_list.html', {'meals': meals})

@login_required
@user_passes_test(is_staff)
def meal_create(request):
    if request.method == 'POST':
        form = MealForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Meal created successfully.')
            return redirect('meal_list')
    else:
        form = MealForm()
    return render(request, 'accounts/meal_form.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def meal_list(request):
    meals = Meal.objects.all()
    return render(request, 'accounts/meal_list.html', {'meals': meals})

@login_required
@user_passes_test(lambda u: u.is_staff)
def meal_create(request):
    if request.method == 'POST':
        form = MealForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Meal created successfully.')
            return redirect('meal_list')
    else:
        form = MealForm()
    return render(request, 'accounts/meal_form.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def meal_update(request, pk):
    meal = get_object_or_404(Meal, pk=pk)
    if request.method == 'POST':
        form = MealForm(request.POST, request.FILES, instance=meal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Meal updated successfully.')
            return redirect('meal_list')
    else:
        form = MealForm(instance=meal)
    return render(request, 'accounts/meal_form.html', {'form': form, 'meal': meal})

@login_required
@user_passes_test(lambda u: u.is_staff)
def meal_delete(request, pk):
    meal = get_object_or_404(Meal, pk=pk)
    if request.method == 'POST':
        meal.delete()
        messages.success(request, 'Meal deleted successfully.')
        return redirect('meal_list')
    return render(request, 'accounts/meal_confirm_delete.html', {'meal': meal})

@login_required
@user_passes_test(is_staff)
def staff_reservation_list(request):
    reservations = Reservation.objects.all().order_by('-date', '-time')
    return render(request, 'accounts/staff_reservation_list.html', {'reservations': reservations})

@login_required
@user_passes_test(is_staff)
def staff_bill_list(request):
    bills = Bill.objects.all().order_by('-created_at')
    return render(request, 'accounts/staff_bill_list.html', {'bills': bills})

def is_staff(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff)
def staff_dashboard(request):
    return render(request, 'accounts/staff_dashboard.html')
