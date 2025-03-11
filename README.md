# CarePoint - Hospital Management System

CarePoint is a hospital management platform designed to facilitate the management of appointments, payments, and prescriptions. The platform supports three types of users: **Staff**, **Doctors**, and **Patients**. The system allows users to register, login, and manage their appointments. Patients can book appointments and make payments via **Stripe**. Doctors can update appointment statuses, and Staff can view all appointment details.

## Features

- **User Roles**: 
  - **Staff**: Can view all appointment details.
  - **Doctors**: Can update appointment statuses (Pending, Cancelled, Confirmed).
  - **Patients**: Can book appointments and make payments.

- **Stripe Payment Integration**: 
  - Patients can pay ₹250 for confirmed appointments.

- **Appointment Management**:
  - Doctors can confirm, cancel, or mark appointments as pending.
  - Patients can view upcoming appointments.

- **Prescription Module**: 
  - A prescription module is added but is not yet functional.

## Installation

To run the CarePoint project locally, follow these steps:

### Prerequisites

- Python 3.x
- Django
- Stripe API keys (for payment functionality)

### Steps to Run the Project Locally

1. Clone the repository:

   git clone https://github.com/yourusername/carepoint.git
   cd carepoint
   
2. Set up a virtual environment (optional but recommended):


python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

3. Install required dependencies:

pip install -r requirements.txt

4. Set up your database:

python manage.py migrate

5. Create a superuser (optional for admin access):

python manage.py createsuperuser

6. Start the development server:

python manage.py runserver

7. Visit http://127.0.0.1:8000 to access the website.


### Configuration

Stripe Integration:

To enable Stripe payments, add your Stripe API keys to settings.py:

STRIPE_SECRET_KEY = 'your-secret-key'
STRIPE_PUBLIC_KEY = 'your-public-key'

How It Works
User Roles
1. Staff:

Staff members can view all appointments in the system.
No modification rights for appointments or payments.

2. Doctors:

Doctors can update the status of appointments to Confirmed, Pending, or Cancelled.
After confirming an appointment, a payment link is provided to the patient.
Doctors can prescribe medications (though the prescription module is not yet active).

3. Patients:

Patients can book appointments with doctors.
Upon confirmation of an appointment, patients can pay a fee of ₹250 for booking.
Payments are processed using the Stripe payment gateway (still in progress).

Stripe Payment Integration

Patients can pay for confirmed appointments, with a payment amount set to ₹250.
Once payment is successfully completed, the system marks the payment as complete, and the appointment status can be updated.
The payment gateway integration is in progress and is not yet fully functional.

### Prescription Module

The prescription module is added to the project but is not yet active.
Once implemented, doctors will be able to prescribe medications during an appointment.

### Future Enhancements

Stripe Payment Gateway: 

Full integration for Stripe payments.

Prescription Module: 

Make the prescription module functional so doctors can provide prescriptions to patients.

Doctor Dashboard: 

Enhance the doctor’s interface to manage appointments and prescriptions.
