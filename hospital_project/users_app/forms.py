from django import forms
from django.contrib.auth.forms import UserCreationForm
from users_app.models import (DOCTOR_SPECIALIZATION_CHOICES,
    STAFF_DEPARTMENT_CHOICES)
from .models import CustomUser, Doctor, Patient, Staff

class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES)

    specialization = forms.ChoiceField(choices=DOCTOR_SPECIALIZATION_CHOICES, required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    mobile = forms.CharField(max_length=15,required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    medical_history = forms.CharField(widget=forms.Textarea, required=False)
    role = forms.CharField(max_length=255, required=False)
    department = forms.ChoiceField(choices=STAFF_DEPARTMENT_CHOICES, required=False)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2','user_type']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = self.cleaned_data.get('user_type')
        
        if commit:
            user.save()
            
        if user.user_type == 'doctor':
            specialization = self.cleaned_data.get('specialization')
            Doctor.objects.create(user=user, specialization=specialization)
        elif user.user_type == 'patient':
            date_of_birth = self.cleaned_data.get('date_of_birth')
            mobile = self.cleaned_data.get('mobile')
            address = self.cleaned_data.get('address')
            medical_history = self.cleaned_data.get('medical_history')
            Patient.objects.create(user=user, date_of_birth=date_of_birth, mobile=mobile, address=address, medical_history=medical_history)
        elif user.user_type == 'staff':
            role = self.cleaned_data.get('role')
            department = self.cleaned_data.get('department')
            Staff.objects.create(user=user, role=role, department=department)

        return user
    
class PatientInformationForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), 
        required=False
    )
    
    class Meta:
        model = Patient
        fields = ['date_of_birth', 'mobile', 'address', 'medical_history']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mobile'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter mobile number'})
        self.fields['address'].widget.attrs.update({'class': 'form-control', 'rows': 3, 'placeholder': 'Enter address'})
        self.fields['medical_history'].widget.attrs.update({'class': 'form-control', 'rows': 3, 'placeholder': 'Enter medical history'})
        
class DoctorInformationForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['specialization']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['specialization'].widget.attrs.update({'class': 'form-control'})
        
class StaffInformationForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['role', 'department']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].widget.attrs.update({'class': 'form-control'})
        self.fields['department'].widget.attrs.update({'class': 'form-control'})
