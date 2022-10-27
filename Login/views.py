from http.client import HTTPResponse
from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
from .forms import   CreateUserForm



def register (request):
    form = CreateUserForm()
    
    if request.method =='POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for '+ user)
            
            return redirect('index')
    
    
    
    context= {'form':form}
    return render(request, "Login/register.html", context)
    
    
    
def index(request):
    
    if request.method== 'POST':
        username= request.POST['username']
        password= request.POST['password']
        fname= user.first_name
        
        user = authenticate(username = username , password=password)
        
        if user is not None:
            login(request, user)
            return render(request, "Login/temp.html", {'fname':fname})
            
        else:
            messages.error(request, "Wrong credentials")
            return redirect(index)
        
    return render(request, "Login/login.html")

def temp(request):
    return render(request, "Login/temp.html")
