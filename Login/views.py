from http.client import HTTPResponse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.
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
