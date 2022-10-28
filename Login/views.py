from http.client import HTTPResponse
from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.
from .forms import   CreateUserForm



def register (request):
    if request.user.is_authenticated:
        return redirect('temp')
    else:
        form = CreateUserForm()
        
        if request.method =='POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for '+ user)
                
                return redirect('loginUser')
        
        
        
        context= {'form':form}
        return render(request, "Login/register.html", context)
        
    
    
def loginUser(request):
    if request.user.is_authenticated:
        return redirect('cs')
    else:
        if request.method== 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request, username=username, password=password)
            
        
            
            if user is not None:
                login(request, user)
                return redirect('cs')
                
            else:
                messages.info(request, 'Username OR password is incorrect')
                
        context = {}    
        return render(request, "Login/login.html", context)

def logoutUser(request):
    logout(request)
    return redirect(loginUser)

@login_required(login_url='login')
def ComputerScience(request):
    return render(request, "Login/cs.html")
