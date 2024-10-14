from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Reservation, Bill, Order, Meal, OrderItem


CustomUser = get_user_model()

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'get_groups']
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('age', 'phone_number', 'address')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('age', 'phone_number', 'address')}),
    )

    def get_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    
    get_groups.short_description = 'Groups'

    actions = ['soft_delete_selected_users']

    def soft_delete_selected_users(self, request, queryset):
        for user in queryset:
            user.soft_delete()
        self.message_user(request, f"{queryset.count()} user(s) have been soft deleted.", messages.SUCCESS)
    soft_delete_selected_users.short_description = "Soft delete selected users"

    def delete_model(self, request, obj):
        obj.soft_delete()
        self.message_user(request, f"User {obj.username} has been soft deleted.", messages.SUCCESS)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.soft_delete()
        self.message_user(request, f"{queryset.count()} user(s) have been soft deleted.", messages.SUCCESS)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Reservation)
admin.site.register(Bill)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Meal)