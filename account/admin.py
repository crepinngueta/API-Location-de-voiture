from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Location, Vehicle, Reservation, Payment, Contact



admin.site.site_header = "Afrique Car Service Administration"
admin.site.site_title = "Afrique Car Service Admin Portal"
admin.site.index_title = "Bienvenue à Afrique Car Service Administration"

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'tc', 'is_admin', 'client', 'owner')
    list_filter = ('is_admin', 'client', 'owner')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'tc', 'client', 'owner', 'id_card_number', 'driving_license_photo', 'profile_picture')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'tc', 'password1', 'password2', 'client', 'owner', 'id_card_number', 'driving_license_photo', 'profile_picture'),
        }),
    )
    search_fields = ('email', 'name', 'id_card_number')
    ordering = ('email',)
    filter_horizontal = ()

class LocationAdmin(admin.ModelAdmin):
    list_display = ('address', 'latitude', 'longitude', 'user')
    search_fields = ('address', 'user__email')
    list_filter = ('user',)

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'owner', 'is_available', 'price_per_day')
    list_filter = ('is_available', 'vehicle_type', 'owner')
    search_fields = ('make', 'model', 'vin')
    ordering = ('-created_at',)

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'client', 'start_date', 'end_date', 'status', 'total_cost')
    list_filter = ('status', 'start_date', 'end_date', 'vehicle')
    search_fields = ('vehicle__make', 'vehicle__model', 'client__email')
    ordering = ('-reservation_date',)

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('reservation', 'amount', 'payment_date', 'payment_method')
    list_filter = ('payment_method', 'payment_date')
    search_fields = ('reservation__id', 'reservation__client__email')
    ordering = ('-payment_date',)

class ContactAdmin(admin.ModelAdmin):
    list_display = ('get_client_name', 'email', 'phone_number', 'created_at')
    search_fields = ('client_contact__name', 'email')
    ordering = ('-created_at',)

admin.site.register(User, UserAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Contact, ContactAdmin)


