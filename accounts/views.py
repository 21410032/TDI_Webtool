from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# Create your views here.
from .forms import ProfileCreationForm,ProfilePictureUpdateForm

def register_view(request):
    if request.method == "POST":
       
        form = ProfileCreationForm(request.POST, request.FILES)  # Include request.FILES here
        if form.is_valid():
            user = form.save()
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password1']
            user = authenticate(request, phone_number=phone_number, password=password)
            login(request, user)
            messages.success(request, 'Registration successful')
            return redirect('home')
    else:
        form = ProfileCreationForm()

    context = {
        'form': form,
    }

    return render(request, 'accounts/register.html', context)




def login_view(request):
    context = {}
    if request.method == "POST":
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        user = authenticate(request, phone_number=phone_number, password=password)
        if user is None:
            messages.error(request, 'Invalid Phone Number or Password')
            return render(request, 'accounts/login.html', context=context)
        login(request, user)
        messages.success(request, 'Successfully logged in')
        return redirect('/')
    
    return render(request, 'accounts/login.html', context=context)

def logout_view(request):
    if request.method == "POST":
        logout(request)
        messages.success(request, 'Successfully logged out')
        return redirect('login')
    
    return render(request, 'accounts/logout.html')


def profile_view(request):

    profile = request.user
    print(profile)

    if request.method == 'POST':
        print('Hello')
        print(request.FILES)
        print(request.POST)
        form = ProfileCreationForm(request.POST, request.FILES, instance=profile)
        print(form)
        if form.is_valid():
            form.save()
            print('hello saved')
            return redirect('accounts/profile.html')
        else:
            print(form.errors)
        
    context = {
        'profile' :profile
    }
    return render (request, 'accounts/profile.html',context)

def profile_edit_view(request):
    if request.method == 'POST':
        form = ProfilePictureUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            # Save only the profile picture field
            request.user.profile_pic = form.cleaned_data['profile_pic']
            request.user.save()

            # Redirect to the profile page or any other page you want
            return redirect('profile')  # Change 'profile' to the actual name of your profile page

    else:
        # If it's a GET request, initialize the form with the current user's data
        form = ProfilePictureUpdateForm(instance=request.user)
    context = {
        
        'form': form,
    }
    return render(request, 'accounts/editprofile.html', context)
    