from django import forms
from .models import Order, Reservation, Meal, OrderItem



class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date', 'time', 'number_of_guests']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = []  # We'll handle the items manually




class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['date', 'time', 'number_of_guests']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['name', 'description', 'price', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = []  # We'll handle the items manually

class OrderItemForm(forms.Form):
    meal = forms.ModelChoiceField(queryset=Meal.objects.all(), widget=forms.HiddenInput())
    quantity = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control quantity-input'}))
 
      

      