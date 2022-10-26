from http.client import HTTPResponse
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "Login/login.html")

#def cs(request):
    #return HTTPResponse("")