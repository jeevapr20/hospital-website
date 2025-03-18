# CarePoint - Hospital Management System

**CarePoint** is a hospital management platform designed to facilitate the management of appointments, payments, and prescriptions. The platform supports three types of users: **Staff**, **Doctors**, and **Patients**. The system allows users to register, login, and manage their appointments. Patients can book appointments and make payments via Stripe. Doctors can update appointment statuses, and Staff can view all appointment details.

## Features

### User Roles:

- **Staff**: Can view all appointment details.
- **Doctors**: Can update appointment statuses (Pending, Cancelled, Confirmed).
- **Patients**: Can book appointments and make payments.

### Stripe Payment Integration:
- Patients can pay ₹250 for confirmed appointments.

### Appointment Management:
- Doctors can confirm, cancel, or mark appointments as pending.
- Patients can view upcoming appointments.

### Prescription Module:
- A prescription module is added but is not yet functional.

## Installation

To run the **CarePoint** project locally or deploy on PythonAnywhere, follow these steps:

### Prerequisites

- Python 3.x
- Django
- Stripe API keys (for payment functionality)

### Steps to Run the Project Locally

1. **Clone the repository**:
   ```bash
   git clone https://github.com/jeevapr20/hospital-website.git
   cd hospital-website
   ```

2. **Set up a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows, use venv\Scripts\activate
   ```

3. **Install required dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your database**:
   - For local development, you can use SQLite (the default database for PythonAnywhere deployment).
   - For PostgreSQL, update the `DATABASES` configuration in `settings.py` during local development, but switch to SQLite for deployment on PythonAnywhere.

   Update `settings.py` to use **SQLite** for deployment:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': BASE_DIR / 'db.sqlite3',  # Path to the SQLite database file
       }
   }
   ```

5. **Run database migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser** (optional for admin access):
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

   Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) to access the website.

---

## Configuration

### Stripe Integration

To enable Stripe payments, add your **Stripe API keys** to `settings.py`:

```python
STRIPE_SECRET_KEY = 'your-secret-key'
STRIPE_PUBLIC_KEY = 'your-public-key'
```

---

## Deployment on PythonAnywhere

To deploy your Django project on **PythonAnywhere** with **SQLite** (the recommended database for free plans), follow these steps:

1. **Create a virtual environment**:
   - On PythonAnywhere, navigate to the "Consoles" tab and open a Bash console.
   - Create and activate a virtual environment:
     ```bash
     python3 -m venv /home/jeeva07/hospital-website/hospitalenv
     source /home/jeeva07/hospital-website/hospitalenv/bin/activate
     ```

2. **Install dependencies**:
   - Upload your `requirements.txt` file to your PythonAnywhere directory.
   - Install the required dependencies:
     ```bash
     pip install -r /home/jeeva07/hospital-website/requirements.txt
     ```

3. **Update `settings.py` for SQLite**:
   - Modify the `DATABASES` section in `settings.py` to use SQLite (as shown in the previous section).

4. **Migrate the database**:
   - Run the migration commands to set up the database:
     ```bash
     python manage.py migrate
     ```

5. **Configure Static Files**:
   - Ensure that the `STATIC_URL`, `STATICFILES_DIRS`, and `STATIC_ROOT` settings are properly configured:
   ```python
   STATIC_URL = '/static/'
   STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
   STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
   ```

6. **Collect Static Files**:
   - On PythonAnywhere, run:
     ```bash
     python manage.py collectstatic
     ```

7. **Configure the WSGI file**:
   - On PythonAnywhere, navigate to the **Web** tab.
   - Set the **Source code** to the path where your project is located, e.g., `/home/jeeva07/hospital-website/`.
   - Configure the **WSGI file** to point to your project:
     ```python
     import os
     import sys

     path = '/home/jeeva07/hospital-website'
     if path not in sys.path:
         sys.path.append(path)

     os.environ['DJANGO_SETTINGS_MODULE'] = 'hospital_project.settings'

     from django.core.wsgi import get_wsgi_application
     application = get_wsgi_application()
     ```

8. **Reload your web app**:
   - After making these changes, click on "Reload" on the PythonAnywhere **Web** tab.

9. **Access the deployed site**:
   - Visit website at `http://jeeva07.pythonanywhere.com/`.

---

## How It Works

### User Roles

- **Staff**: Staff members can view all appointments in the system. No modification rights for appointments or payments.
- **Doctors**: Doctors can update the status of appointments to Confirmed, Pending, or Cancelled. After confirming an appointment, a payment link is provided to the patient. Doctors can prescribe medications (though the prescription module is not yet active).
- **Patients**: Patients can book appointments with doctors. Upon confirmation of an appointment, patients can pay a fee of ₹250 for booking. Payments are processed using the Stripe payment gateway.

---

## Future Enhancements

1. **Prescription Module**:
   - Make the prescription module functional so doctors can provide prescriptions to patients.

2. **Doctor Dashboard**:
   - Enhance the doctor’s interface to manage appointments and prescriptions.

