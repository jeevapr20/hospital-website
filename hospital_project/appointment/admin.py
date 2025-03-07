from django.contrib import admin
from .models import Appointment, Prescription, Payment

# Appointment Admin
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'appointment_date', 'status', 'created_at', 'updated_at')
    search_fields = ('doctor__user__first_name', 'doctor__user__last_name', 'patient__user__first_name', 'patient__user__last_name')

admin.site.register(Appointment, AppointmentAdmin)

# Prescription Admin
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'prescribed_by', 'created_at')
    search_fields = ('appointment__patient__user__first_name', 'appointment__patient__user__last_name', 'prescribed_by__user__first_name')

admin.site.register(Prescription, PrescriptionAdmin)

# Payment Admin
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'amount', 'payment_method', 'status', 'payment_date')
    search_fields = ('appointment__patient__user__first_name', 'appointment__patient__user__last_name', 'payment_method')

admin.site.register(Payment, PaymentAdmin)