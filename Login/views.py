from http.client import HTTPResponse
from multiprocessing import context
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import *
from Login.models import *

# Create your views here.
from .forms import CreateUserForm


def register(request):
    if request.user.is_authenticated:
        return redirect('temp')
    else:
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('loginUser')

        context = {'form': form}
        return render(request, "Login/register.html", context)


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('cs')
    else:
        if request.method == 'POST':
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
    examresult = ExamResult.objects.filter(department_id='2').values
    courses = Course.objects.all()
    csstudents = Student.objects.filter(department_id='2')
    return render(request, "Login/cs.html", {'student': csstudents, 'course': courses, 'Examresult': examresult})


def AddStudent(request):
    form = Add()
    if request.method == 'POST':

        form = Add(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}

    return render(request, "Login/AddStudent.html", context)


def UpdateStudent(request, pk):
    student = Student.objects.get(id=pk)
    form = Add(instance=student)

    if request.method == 'POST':

        form = Add(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, "Login/UpdateStudent.html", context)


def DeleteStudent(request, pk):
    student = Student.objects.get(id=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('/')

    context = {'student': student}
    return render(request, "Login/DeleteStudent.html", context)
