from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import stripe
from .forms import AppointmentBookingForm, AppointmentStatusForm
from .models import Appointment, Payment
from users_app.models import Doctor, Patient

@login_required
def update_appointment_status(request, appointment_id):
    # Fetch the appointment using the provided appointment_id
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Ensure the logged-in user is the doctor assigned to the appointment
    if not request.user.is_staff and appointment.doctor.user != request.user:
        return redirect('error')  # Redirect to a safe page if user is not authorized

    if request.method == 'POST':
        form = AppointmentStatusForm(request.POST, instance=appointment)
        if form.is_valid():
            appointment = form.save()  # Save the updated status
            print(f"Updated appointment status: {appointment.status}")
            
            # If the appointment status is confirmed
            if appointment.status == 'confirmed':
                # If the logged-in user is not a doctor (i.e., patient), redirect to payment session
                if appointment.patient.user == request.user:
                    print(f"Redirecting patient to payment session for appointment {appointment.id}")
                    return redirect('create_payment_session', appointment_id=appointment.id)
                else:
                    # If the user is a doctor, just stay on the same page (no redirect to payment)
                    print(f"Doctor confirmed appointment, staying on the same page.")
                    return redirect('doctor_dashboard')
            
            # If the status is not confirmed, simply return to doctor dashboard
            return redirect('doctor_dashboard')
        else:
            print(f"Form Errors: {form.errors}")
    else:
        form = AppointmentStatusForm(instance=appointment)  # Pre-fill the form with current status

    return render(request, 'appointment/appointment_status.html', {'form': form, 'appointment': appointment})


@login_required
def book_appointment(request):
    try:
        patient = request.user.patient  # Ensure the logged-in user has a related Patient instance
    except Patient.DoesNotExist:
        return redirect('error')  # Redirect if no patient is found for the user

    if request.method == 'POST':
        form = AppointmentBookingForm(request.POST, user=request.user)
        if form.is_valid():
            appointment = form.save()
            patient.update_appointments_count()  # If there's a count logic for the patient's appointments

            # Check if appointment status is confirmed immediately after booking
            if appointment.status == 'confirmed':
                return redirect('create_payment_session', appointment_id=appointment.id)
            else:
                return redirect('patient_dashboard')  # Or any other redirect after booking
        else:
            return render(request, 'appointment/book_appointment.html', {'form': form})

    else:
        form = AppointmentBookingForm(user=request.user)
    return render(request, 'appointment/book_appointment.html', {'form': form})

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def create_payment_session(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Check if the logged-in user is the patient for this appointment
    if appointment.patient.user != request.user:
        return redirect('error')

    try:
        # Create a new Stripe session for the appointment
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': f'Appointment with {appointment.doctor.user.full_name}',
                    },
                    'unit_amount': 250 * 100,  # Convert ₹250 to cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url = request.build_absolute_uri(reverse('payment_success', args=[appointment.id])),
            cancel_url = request.build_absolute_uri(reverse('payment_cancel', args=[appointment.id])),
        )
        
        # Debugging: log the session URL
        print(session.url)


        # Return the session ID as JSON
        return JsonResponse({'sessionId': session.id})

    except stripe.error.StripeError as e:
        return JsonResponse({'error': str(e)})
    
@login_required
def payment_success(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Update payment status
    appointment.payment_status = 'completed'
    appointment.save()

    Payment.objects.create(appointment=appointment, status='completed', amount=250)

    return render(request, 'appointment/payment_success.html', {'appointment': appointment})



@login_required
def payment_cancel(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    return render(request, 'appointment/payment_cancel.html', {'appointment': appointment})

@login_required
def upcoming_appointments(request):
    # Fetch the patient's upcoming appointments
    patient = request.user.patient
    appointments = Appointment.objects.filter(patient=patient, appointment_date__gte=timezone.now())

    return render(request, 'appointment/upcoming_appointments.html', {'appointments': appointments})

@login_required
def appointment_status(request, appointment_id):
    # Fetch the appointment using the provided appointment_id
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Ensure the logged-in user is the doctor assigned to the appointment
    if appointment.doctor.user != request.user:
        return redirect('doctor_dashboard')  # Or another appropriate page

    if request.method == 'POST':
        form = AppointmentStatusForm(request.POST, instance=appointment)
        if form.is_valid():
            appointment = form.save()  # Save the updated status
            print(f"Updated appointment status: {appointment.status}")
            
            # If the appointment status is confirmed
            if appointment.status == 'confirmed':
                # If the logged-in user is a patient, redirect to payment session
                if appointment.patient.user == request.user:
                    print(f"Redirecting patient to payment session for appointment {appointment.id}")
                    return redirect('create_payment_session', appointment_id=appointment.id)
                else:
                    # If the user is a doctor, just stay on the same page (no redirect to payment)
                    print(f"Doctor confirmed appointment, staying on the same page.")
                    return render(request, 'appointment/appointment_status.html', {'form': form, 'appointment': appointment})

            return redirect('doctor_dashboard')  # Or other redirect for pending/canceled statuses
        else:
            print(f"Form Errors: {form.errors}")
    else:
        form = AppointmentStatusForm(instance=appointment)  # Pre-fill the form with current status

    return render(request, 'appointment/appointment_status.html', {'form': form, 'appointment': appointment})


    
@login_required
def doctor_appointments(request):
    try:
        doctor = request.user.doctor
        appointments = Appointment.objects.filter(doctor=doctor, appointment_date__gte=timezone.now()).order_by('appointment_date')
        for appointment in appointments:
            appointment.form = AppointmentStatusForm(instance=appointment)
    except Doctor.DoesNotExist:
        return redirect('error')

    return render(request, 'appointment/doctor_appointments.html', {'doctor': doctor, 'appointments': appointments})

#staff
@login_required
def all_appointments(request):

    appointments = Appointment.objects.all()
    return render(request, 'appointment/all_appointments.html', {'appointments': appointments})
