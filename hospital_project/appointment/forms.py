from django import forms

from users_app.models import Doctor, Patient
from .models import Appointment

class AppointmentStatusForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=Appointment.APPOINTMENT_STATUS_CHOICES, attrs={'class': 'form-control'})
        }

        
class AppointmentBookingForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all())
    appointment_date = forms.DateTimeField(widget=forms.DateInput(attrs={'type': 'datetime-local', 'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), required=False)
    
    # Adding patient fields for display (readonly)
    patient_name = forms.CharField(max_length=255, disabled=True, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    patient_email = forms.EmailField(disabled=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
    patient_mobile = forms.CharField(max_length=15, disabled=True, widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))

    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'description']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Retrieve the user
        super(AppointmentBookingForm, self).__init__(*args, **kwargs)

        # Auto-fill the fields with patient data
        if self.user and hasattr(self.user, 'patient'):
            patient = self.user.patient
            self.fields['patient_name'].initial = patient.user.full_name
            self.fields['patient_email'].initial = self.user.email
            self.fields['patient_mobile'].initial = patient.mobile

        # Add custom styling
        self.fields['doctor'].widget.attrs.update({'class': 'form-control'})
        self.fields['appointment_date'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        appointment = super().save(commit=False)
        appointment.patient = self.user.patient  # Ensure the patient is set correctly
        if commit:
            appointment.save()
        return appointment
