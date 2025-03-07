from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
from .models import Doctor, Patient, Staff
from .forms import PatientInformationForm, DoctorInformationForm, StaffInformationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def custom_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            if user.user_type == 'doctor':
                return redirect('doctor_dashboard')  
            elif user.user_type == 'patient':
                return redirect('patient_dashboard')
            elif user.user_type == 'staff':
                return redirect('staff_dashboard')
        else:
            form.add_error(None, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'users_app/login.html', {'form': form})


def custom_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            login(request, user)
            
            messages.success(request, "Registration successful! You can now log in.")
          
            return redirect('login')
        
        else:
            form.add_error(None, "Please correct the below errors.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'users_app/register.html', {'form': form})


@login_required
def personal_information(request):
    user = request.user
    user_type = user.user_type 

  
    if user_type == 'patient':
        if request.method == 'POST':
            form = PatientInformationForm(request.POST, instance=user.patient)  # pre-fill instance with existing data
            if form.is_valid():
                form.save()
                return redirect('patient_dashboard') 
        else:
            form = PatientInformationForm(instance=user.patient)

    elif user_type == 'doctor':
        if request.method == 'POST':
            form = DoctorInformationForm(request.POST, instance=user.doctor)
            if form.is_valid():
                form.save()
                return redirect('doctor_dashboard')
        else:
            form = DoctorInformationForm(instance=user.doctor)

    elif user_type == 'staff':
        if request.method == 'POST':
            form = StaffInformationForm(request.POST, instance=user.staff)
            if form.is_valid():
                form.save()
                return redirect('staff_dashboard')
        else:
            form = StaffInformationForm(instance=user.staff)

    return render(request, 'users_app/personal_information.html', {'form': form})

@login_required
def doctor_dashboard(request):
    try:
        doctor = request.user.doctor
    except Doctor.DoesNotExist:
        return redirect('error')  

    return render(request, 'users_app/doctor_dashboard.html', {'doctor': doctor})

@login_required
def patient_dashboard(request):
    # Get the logged-in patient's data
    patient = request.user.patient  # Assuming each user has one related Patient
    appointments = patient.appointment_set.all()  # Get all appointments for the patient

    return render(request, 'users_app/patient_dashboard.html', {
        'patient': patient,
        'appointments': appointments,
    })



def staff_dashboard(request):
    staff = Staff.objects.get(user=request.user)
   
    return render(request, 'users_app/staff_dashboard.html', {'staff': staff})

def custom_logout(request):
    logout(request)
    return redirect('login')