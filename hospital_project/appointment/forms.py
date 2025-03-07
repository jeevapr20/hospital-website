from django import forms

from users_app.models import Doctor, Patient
from .models import Appointment

class AppointmentStatusForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['status']
        widgets = {
            'status': forms.Select(choices=Appointment.APPOINTMENT_STATUS_CHOICES),
        }
        
class AppointmentBookingForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all())
    appointment_date = forms.DateTimeField(widget=forms.DateInput(attrs={'type': 'datetime-local'}))
    description = forms.CharField(widget=forms.Textarea, required=False)
    
    # Adding patient fields for display (readonly)
    patient_name = forms.CharField(max_length=255, disabled=True)
    patient_email = forms.EmailField(disabled=True)
    patient_mobile = forms.CharField(max_length=15, disabled=True)

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

    def save(self, commit=True):
        appointment = super().save(commit=False)
        appointment.patient = self.user.patient  # Ensure the patient is set correctly
        if commit:
            appointment.save()
        return appointment