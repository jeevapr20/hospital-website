from django.db import models
from users_app.models import Patient, Doctor

class Appointment(models.Model):
    APPOINTMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=APPOINTMENT_STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Appointment for {self.patient.user.full_name} with {self.doctor.user.full_name} on {self.appointment_date}"
        
class Prescription(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)  
    prescribed_by = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    medication = models.TextField() 
    dosage = models.TextField()  
    instructions = models.TextField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Prescription for {self.appointment.patient.user.full_name} on {self.created_at}"

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2) 
    payment_method = models.CharField(max_length=100) 
    status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment for Appointment {self.appointment.id} - {self.status}"
    
    