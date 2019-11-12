from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account successfully created! for {username}\
            Please log in with you new username and password')
            return redirect('User-Login')
    else:
        form = UserRegisterForm()
    return render(request, 'Users/register.html', {'form': form})


@login_required     # Add functionality to an existing function
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance = request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(request, f'Account successfully updated')
            return redirect('User-Profile')
    else:
        u_form = UserUpdateForm(instance = request.user)
        p_form = ProfileUpdateForm(instance = request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
     }

    from django.http import HttpResponse as response
    response('<h1>{{}}</h1>')
    return render(request, 'Users/profile.html', context, {'title': 'Profile'})


@login_required
def adminLogout(request):
    return redirect('FittingRoom-Home')


@login_required
def upload_dress(request):
    context = {  }
    if request.method == 'POST':
        dress = request.FILES['dress_image']
        save_file_url = settings.UPLOAD_ROOT + '/users/' + request.user.username + '/' + 'dresses/'
        print(save_file_url)
        upload_storage = FileSystemStorage(location = save_file_url, base_url = settings.UPLOAD_ROOT)
        name = upload_storage.save(dress.name, dress)
        context['url'] = upload_storage.url(name)
    return render(request, 'Users/upload.html')


@login_required
def delete_profile_confirmation(request):
    return render(request, 'Users/user_delete_confirmation.html', {'title': 'Delete Confirmation'})


@login_required
def delete_profile(request):
    try:
        u = User.objects.get(username = request.user.username);
        u.delete()
        messages.error(request, f"{ username } is deleted")
        print('User successfully deleted')

    except User.DoesNotExist:
        messages.error(request, f"{ username } does not exist")
        print('User does not exist')
        return render(request, 'FittingRoom/home.html', {'title': 'Home'})

    except Exception as e:
        print('Unknown error occurred')
        return render(request, 'Users/logout.html', {'title': 'Home'})

    return render(request, 'Users/logout.html', {'title': 'Home'})
