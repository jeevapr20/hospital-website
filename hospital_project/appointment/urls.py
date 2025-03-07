from django.urls import path
from . import views

urlpatterns = [
    path('book_appointment/', views.book_appointment, name='book_appointment'),
    path('appointment/status/<int:appointment_id>/', views.appointment_status, name='appointment_status'),
    path('create_payment_session/<int:appointment_id>/', views.create_payment_session, name='create_payment_session'),
    path('payment_success/<int:appointment_id>/', views.payment_success, name='payment_success'),
    path('payment_cancel/<int:appointment_id>/', views.payment_cancel, name='payment_cancel'),
    path('upcoming_appointments/', views.upcoming_appointments, name='upcoming_appointments'),
    path('doctor_appointments/', views.doctor_appointments, name='doctor_appointments'),
    path('all_appointments/', views.all_appointments, name='all_appointments'),
]
