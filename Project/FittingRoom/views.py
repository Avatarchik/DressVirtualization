from django.shortcuts import render
from django.http import HttpResponse as response

def home(request):
    if request.user.is_authenticated:
        return render(request, 'FittingRoom/home.php', { 'title': 'Home' })
    else:
        return render(request, 'FittingRoom/default_home.php', { 'title': 'Home' })


def display_model(request):
    return render(request, 'FittingRoom/model.html', { 'title': 'Our Model' })


def contact(request):
    return render(request, 'FittingRoom/contact.html', { 'title': 'Contact' })
