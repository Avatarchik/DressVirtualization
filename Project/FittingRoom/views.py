from django.shortcuts import render
from django.http import HttpResponse as response
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.conf import settings
import os

def home(request):
    if request.user.is_authenticated:
        return render(request, 'FittingRoom/home.html', { 'title': 'Home' })
    else:
        return render(request, 'FittingRoom/default_home.html', { 'title': 'Home' })


def display_model(request):
    return render(request, 'FittingRoom/model.html', { 'title': 'Our Model' })


def contact(request):
    return render(request, 'FittingRoom/contact.html', { 'title': 'Contact' })


@csrf_exempt
def dress_library(request):
    files_list, context = [], {}
    for filename in os.listdir(os.path.join(settings.STATIC_ROOT, 'FittingRoom/Dresses')):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            files_list.append(filename)
    for i in range(len(files_list)):
        key, value = str(i), filename
        context[key] = value

    print(f'Dictionary: {context}')

    try:
        return render(request, 'FittingRoom/home.html', context, {'title': 'Test'})
    except:
        print("An error had occurred")
        return render(request, 'FittingRoom/home.html', {'title:': 'Test'})
