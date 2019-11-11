from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    width = forms.CharField(required = False)
    height = forms.CharField(required = False)

    class Meta:
        model = User
        fields = [ 'username', 'email', 'width', 'height', 'password1', 'password2' ]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    width = forms.CharField(required = False)
    height = forms.CharField(required = False)

    class Meta:
        model = User
        fields = [ 'username', 'email', 'width', 'height']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']
