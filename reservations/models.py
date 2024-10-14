from django.db import models

# Create your models here.

from django.conf import settings

class Reservation(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    table_number = models.PositiveIntegerField()
    date = models.DateField()
    time = models.TimeField()
    number_of_guests = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['table_number', 'date', 'time']

    def __str__(self):
        return f"Reservation for {self.customer.username} on {self.date} at {self.time}"