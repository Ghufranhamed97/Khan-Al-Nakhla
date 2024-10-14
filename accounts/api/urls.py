from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeAPIView.as_view(), name='api_home'),
    path('register/', views.RegisterAPIView.as_view(), name='api_register'),
    path('login/', views.LoginAPIView.as_view(), name='api_login'),
    path('logout/', views.LogoutAPIView.as_view(), name='api_logout'),
    path('reserve/', views.ReserveTableAPIView.as_view(), name='api_reserve_table'),
    path('order/', views.OrderMealAPIView.as_view(), name='api_order_meal'),
    path('reservations/', views.ReservationListAPIView.as_view(), name='api_reservation_list'),
    path('bills/', views.BillListAPIView.as_view(), name='api_bill_list'),
    path('bills/<int:bill_id>/', views.BillDetailAPIView.as_view(), name='api_bill_detail'),
]