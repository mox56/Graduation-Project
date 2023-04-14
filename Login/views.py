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


@api_view(['GET'])
def StudentDetail(request, pk):
    queryset = Student.objects.get(student_index=pk)
    serializer_class = StudentSerializer(queryset)
    return Response(serializer_class.data)


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


@login_required(login_url='login')
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)

            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, "Login/register.html", {'form': form})


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('DataEntry')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_dataentry:
                login(request, user)
                return redirect('DataEntry')

            elif user is not None and user.is_registrar:
                login(request, user)
                return redirect('Registrar')

            else:
                messages.info(
                    request, 'Username OR password is incorrect OR your not allowed to view page.')

        context = {}
        return render(request, "Login/login.html", context)


def logoutUser(request):
    logout(request)
    return redirect(loginUser)


@login_required(login_url='login')
def DataEntry(request):
    # examresult = ExamResult.objects.filter(department_id='2')
    examresult = ExamResult.objects.all()
    courses = Course.objects.all()
    students = Student.objects.all()
    # csstudents = Student.objects.filter(department_id='2')

    # myFilter = SemesterFilter(request.GET, queryset=csstudents)
    # csstudents = myFilter.qs

    return render(request, "Login/DataEntry.html", {'student': students, 'course': courses, 'Examresult': examresult})


@login_required(login_url='login')
def Registrar(request):
    students = Student.objects.all()
    return render(request, "Login/Registrar.html", {'student': students})


def AddStudent(request):
    form = StudentForm()
    if request.method == 'POST':

        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Registrar')

    context = {'form': form}

    return render(request, "Login/AddStudent.html", context)


def UpdateStudent(request, pk):
    student = Student.objects.get(student_index=pk)
    form = StudentForm(instance=student)
    student.value = pk
    if request.method == 'POST':

        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save(['value'])
            return redirect('Registrar')

    context = {'form': form}
    return render(request, "Login/UpdateStudent.html", context)


def DeleteStudent(request, pk):
    student = Student.objects.get(student_index=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('/')

    context = {'student': student}
    return render(request, "Login/DeleteStudent.html", context)


def AddResult(request):
    form = ExamForm()
    if request.method == 'POST':

        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Dataentry')

    context = {'form': form}

    return render(request, "Login/AddResult.html", context)


def UpdateResult(request, pk):
    examresult = ExamResult.objects.get(student_index=pk)
    form = ExamForm(instance=examresult)
    examresult.value = pk
    if request.method == 'POST':

        form = ExamForm(request.POST, instance=examresult)
        if form.is_valid():
            form.save(['value'])
            return redirect('DataEntry')

    context = {'form': form}
    return render(request, "Login/UpdateResult.html", context)


def DeleteResult(request, pk):
    examresult = ExamResult.objects.get(student_index=pk)
    if request.method == 'POST':
        examresult.delete()
        return redirect('/')

    context = {'examresult': examresult}
    return render(request, "Login/DeleteResult.html", context)
