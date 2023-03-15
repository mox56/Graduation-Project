from http.client import HTTPResponse
from multiprocessing import context
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from Login.Permissions import IsOwnerOrReadOnly
from rest_framework import permissions
from rest_framework.reverse import reverse
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from django.http import Http404
from rest_framework import renderers
from rest_framework.views import APIView
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import *
from rest_framework import mixins
from rest_framework import generics
from Login.models import *
from Login.serializers import StudentSerializer, UserSerializer
from .filters import SemesterFilter
# Create your views here.


@api_view(['GET'])
def getStudent(request):
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)


class StudentList(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('student_index')
    serializer_class = StudentSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


def register(request):
    if request.user.is_authenticated:
        return redirect('temp')
    else:
        form = UserSerializer()

        if request.method == 'POST':
            form = UserSerializer(request.POST)
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
    examresult = ExamResult.objects.filter(department_id='2')
    courses = Course.objects.all()
    csstudents = Student.objects.filter(department_id='2')

    myFilter = SemesterFilter(request.GET, queryset=csstudents)
    csstudents = myFilter.qs

    return render(request, "Login/cs.html", {'student': csstudents, 'course': courses, 'Examresult': examresult, 'myFilter': myFilter})


def AddStudent(request):
    form = StudentForm()
    if request.method == 'POST':

        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}

    return render(request, "Login/AddStudent.html", context)


def UpdateStudent(request, pk):
    student = Student.objects.get(student_index=pk)
    form = StudentForm(instance=student)

    if request.method == 'POST':

        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, "Login/UpdateStudent.html", context)


def DeleteStudent(request, pk):
    student = Student.objects.get(student_index=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('/')

    context = {'student': student}
    return render(request, "Login/DeleteStudent.html", context)
