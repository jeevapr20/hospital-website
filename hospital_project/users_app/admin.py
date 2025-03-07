from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Doctor, Staff, Patient

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('user_type', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
admin.site.register(CustomUser, CustomUserAdmin)

# Doctor Admin
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'created_at', 'updated_at')
    search_fields = ('user__first_name', 'user__last_name', 'specialization')
    list_filter = ('user__user_type', 'specialization', 'created_at')

admin.site.register(Doctor, DoctorAdmin)

# Staff Admin
class StaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'department', 'created_at', 'updated_at')
    search_fields = ('user__first_name', 'user__last_name', 'role', 'department')
    list_filter = ('user__user_type', 'role', 'department', 'created_at')

admin.site.register(Staff, StaffAdmin)

# Patient Admin
class PatientAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'created_at', 'updated_at')
    search_fields = ('user__first_name', 'user__last_name', 'date_of_birth')
    list_filter = ('user__user_type', 'date_of_birth', 'created_at')

admin.site.register(Patient, PatientAdmin)