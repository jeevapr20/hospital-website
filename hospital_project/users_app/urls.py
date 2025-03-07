from django.urls import path
from . import views

urlpatterns = [
        path('login/', views.custom_login, name='login'),
        path('register/', views.custom_register, name='register'),
        path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
        path('patient_dashboard/', views.patient_dashboard, name='patient_dashboard'),
        path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
        path('personal-information/', views.personal_information, name='personal-information'),
        path('logout/', views.custom_logout, name='logout'),
        
]