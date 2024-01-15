from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class ProfileCreationForm(UserCreationForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2', 'profile_pic']