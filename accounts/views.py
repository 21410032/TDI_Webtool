from django.shortcuts import render
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
# Create your views here.

def register_view(request):
  if request.method == "POST":
    form=UserCreationForm(request.POST or None)
    if form.is_valid():
       form.save()
       username = form.cleaned_data['username']
       password = form.cleaned_data['password1']
       user = authenticate(username=username, password=password)
       login(request, user)
       messages.success(request, ('Registration successfull'))
       return redirect('home')
    
  else:
     form = UserCreationForm()
       
  context={
  "form":form
  }
 
  return render(request,'accounts/register.html',context)








def login_view(request):
    context ={}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username,password=password)
        if user is None:
            messages.success(request, ('Invalid Username or Password'))
            return render(request,'accounts/login.html',context=context)
        login(request,user)
        messages.success(request, ('Successfully logged in'))
        return redirect('/')

    return render(request,'accounts/login.html',context=context)

def logout_view(request):

    if request.method == "POST":
        logout(request)
        messages.success(request, ('Successfully logged out'))
        return redirect('login')
    return render(request,'accounts/logout.html')
    