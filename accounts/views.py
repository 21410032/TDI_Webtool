from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# Create your views here.
from .forms import ProfileCreationForm

def register_view(request):
    if request.method == "POST":
        form = ProfileCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password1']  # Use password1 for the first password field
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
    context = {
        'profile' :profile
    }
    return render (request, 'accounts/profile.html',context)


    