from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class ProfileCreationForm(UserCreationForm):
    phone_number = forms.IntegerField(required=True)
    email = forms.EmailField(required=True)
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'password1', 'password2', 'profile_pic']

    def save(self, commit=True):
        profile = super().save(commit=False)

        # Handle the profile picture
        if 'profile_pic' in self.cleaned_data:
            profile.profile_pic = self.cleaned_data['profile_pic']

        if commit:
            profile.save()

        return profile
    

class ProfilePictureUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic']