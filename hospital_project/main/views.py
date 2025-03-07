from django.shortcuts import render

# Create your views here.
def base(request):
    return render(request,"base.html")

def testimony(request):
    return render(request,"main/testimonial.html")

def service(request):
    return render(request,"main/service.html")

def team(request):
    return render(request,"main/team.html")

def about(request):
    return render(request,"main/about.html")

def contact(request):
    return render(request,"main/contact.html")

def feature(request):
    return render(request,"main/feature.html")

def appointment(request):
    return render(request,"main/appointment.html")

def error(request):
    return render(request,"main/404.html")