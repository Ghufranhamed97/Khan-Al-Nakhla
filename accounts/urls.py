from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('login/success/', views.login_success, name='login_success'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('reserve/', views.reserve_table, name='reserve_table'),
    path('order/', views.order_meal, name='order_meal'),
    path('reservations/', views.reservation_list, name='reservation_list'),
    path('reservations/update/<int:pk>/', views.update_reservation, name='update_reservation'),
    path('bills/', views.bill_list, name='bill_list'),
    path('bills/<int:bill_id>/', views.bill_detail, name='bill_detail'),
    path('meals/', views.meal_list, name='meal_list'),
    path('meals/create/', views.meal_create, name='meal_create'),
    path('meals/<int:pk>/update/', views.meal_update, name='meal_update'),
    path('meals/<int:pk>/delete/', views.meal_delete, name='meal_delete'),
    path('staff/reservations/', views.staff_reservation_list, name='staff_reservation_list'),
    path('staff/bills/', views.staff_bill_list, name='staff_bill_list'),
    path('bill/<int:bill_id>/', views.bill_detail, name='bill_detail'),
    
    
]
    
    

