from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('staff', 'Staff'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES,db_index=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return self.full_name
    
DOCTOR_SPECIALIZATION_CHOICES = [
    ('cardiology', 'Cardiology'),
    ('dentistry', 'Dentistry'),
    ('orthopedics', 'Orthopedics'),
    ('neurology', 'Neurology'),
    ('pediatrics', 'Pediatrics'),
    ('general_practice', 'General Practice'),
    ('gynecology', 'Gynecology'),
    ('dermatology', 'Dermatology'),
]

class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)  #OneToOne field avoids duplicate names
    specialization = models.CharField(max_length=100, choices=DOCTOR_SPECIALIZATION_CHOICES, default='general_practice')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.full_name} ({self.specialization})"

class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    mobile = models.CharField(max_length=15,blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    medical_history = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.full_name}"
    
    def update_appointments_count(self):
        self.total_appointments = self.appointment_set.count()  # Assuming reverse relation from Appointment to Patient
        self.save()

STAFF_DEPARTMENT_CHOICES = [
    ('admin', 'Administration'),
    ('finance', 'Finance'),
    ('hr', 'Human Resources'),
    ('nursing', 'Nursing'),
    ('it', 'Information Technology'),
    ('maintenance', 'Maintenance'),
    ('support', 'Support'),
    ('medical', 'Medical'),
    ('reception', 'Reception'),
   
]

class Staff(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=255)
    department = models.CharField(max_length=100, choices=STAFF_DEPARTMENT_CHOICES, default='admin')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.full_name} ({self.role})"
