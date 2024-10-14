from rest_framework import serializers
from .models import CustomUser, Reservation, Bill, Order, Meal, OrderItem

class CustomUserSerializer(serializers.ModelSerializer):
       class Meta:
           model = CustomUser
           fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'address', 'age']

class ReservationSerializer(serializers.ModelSerializer):
       class Meta:
           model = Reservation
           fields = '__all__'

class MealSerializer(serializers.ModelSerializer):
       class Meta:
           model = Meal
           fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
       class Meta:
           model = OrderItem
           fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
       items = OrderItemSerializer(many=True, read_only=True)

       class Meta:
           model = Order
           fields = '__all__'

class BillSerializer(serializers.ModelSerializer):
       class Meta:
           model = Bill
           fields = '__all__'