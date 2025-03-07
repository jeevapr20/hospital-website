from django.urls import path
from . import views

urlpatterns = [
        path('', views.base, name='home'),
        path('testimony/',views.testimony,name="testimony"),
        path('service/',views.service,name="service"),
        path('team/',views.team,name="team"),
        path('about/',views.about,name="about"),
        path('contact/',views.contact,name="contact"),
        path('feature/',views.feature,name="feature"),
        path('appointment/',views.appointment,name="appointment"),
        path('error/',views.error,name="error"),
]