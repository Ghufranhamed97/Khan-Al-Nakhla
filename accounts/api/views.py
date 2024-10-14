from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout
from ..models import CustomUser, Reservation, Bill, Order, Meal, OrderItem
from .serializers import CustomUserSerializer, ReservationSerializer, BillSerializer, OrderSerializer, MealSerializer
from rest_framework import permissions

class HomeAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return Response({"message": "Welcome to Khan Al-Nakhla API"})

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return Response({"message": "Login successful"})
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"})

class ReserveTableAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderMealAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        meals = Meal.objects.all().order_by('category', 'name')
        serializer = MealSerializer(meals, many=True)
        return Response(serializer.data)

    def post(self, request):
        order = Order.objects.create(customer=request.user, total_price=0)
        total_price = 0
        
        for meal_id, quantity in request.data.items():
            meal = Meal.objects.get(id=meal_id)
            OrderItem.objects.create(order=order, meal=meal, quantity=quantity)
            total_price += meal.price * quantity
        
        order.total_price = total_price
        order.save()
        
        bill = Bill.objects.create(customer=request.user, order=order, amount=total_price)
        
        return Response({
            "message": "Order placed successfully",
            "bill_id": bill.id,
            "total_price": total_price
        }, status=status.HTTP_201_CREATED)

class IsStaffOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.customer == request.user

class ReservationListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsStaffOrOwner]
    def get(self, request):
        if request.user.is_staff:
            reservations = Reservation.objects.all()
        else:
            reservations = Reservation.objects.filter(customer=request.user)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

class BillListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        bills = Bill.objects.filter(customer=request.user)
        serializer = BillSerializer(bills, many=True)
        return Response(serializer.data)

class BillDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, bill_id):
        try:
            bill = Bill.objects.get(id=bill_id, customer=request.user)
            serializer = BillSerializer(bill)
            return Response(serializer.data)
        except Bill.DoesNotExist:
            return Response({"error": "Bill not found"}, status=status.HTTP_404_NOT_FOUND)

class ReservationCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(customer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MealListAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        meals = Meal.objects.all()
        serializer = MealSerializer(meals, many=True)
        return Response(serializer.data)

class OrderCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        order = Order.objects.create(customer=request.user, total_price=0)
        total_price = 0
        
        for meal_id, quantity in request.data.items():
            meal = Meal.objects.get(id=meal_id)
            OrderItem.objects.create(order=order, meal=meal, quantity=quantity)
            total_price += meal.price * quantity
        
        order.total_price = total_price
        order.save()
        
        bill = Bill.objects.create(customer=request.user, order=order, amount=total_price)
        
        return Response({
            "message": "Order placed successfully",
            "bill_id": bill.id,
            "total_price": total_price
        }, status=status.HTTP_201_CREATED)