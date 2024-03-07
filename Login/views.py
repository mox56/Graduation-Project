from http.client import HTTPResponse
from multiprocessing import context
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from Login.Permissions import IsOwnerOrReadOnly
from rest_framework import permissions
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated
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
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework import generics, status
from Login.models import *
from Login.serializers import *
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer, RegisterSerializer
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework. response import Response
from rest_framework.request import Request
# Create your views here.


@api_view(['POST'])
def logintest(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    return Response({"token": token.key, "user": serializer.data})


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    return Response("passed for {}".format(request.user.username))


@api_view(['POST'])
def signuptest(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(APIView):
    permission_classes = []

    def post(self, request: Request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            response = {
                "message": "Login successfull",
                "token": user.auth_token.key
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data={"message": "Invalid username or password"})

    def get(self, request: Request):
        content = {
            "user": str(request.user),
            "auth": str(request.auth)
        }

        return Response(data=content, status=status.HTTP_200_OK)

# Register API


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request: Request):
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            response = {
                "message": "User Created Successfully",
                "data": serializer.data
            }

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

@api_view(['GET', 'PUT', 'DELETE'])
def exam_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        exam = ExamResult.objects.get(pk=pk)
    except ExamResult.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ExamSerializer(exam)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ExamSerializer(exam, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        exam.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ExamView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = ExamSerializer
    def get (self, request,pk):
        single_exam = ExamResult.objects.get(id = pk)
        serializers = ExamSerializer(single_exam)
        return Response(serializers.data)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()

        # Assuming you have a serializer for ExamResult
        exam_serializer = ExamSerializer(data=request.data, partial=True)
        exam_serializer.is_valid(raise_exception=True)

        # Find the exam instance based on the provided 'id'
        exam_id = exam_serializer.validated_data['id']
        
        # Access the related set of exams for the specific student
        exam_instance = instance.Exams_Results.get(id=exam_id)

        # Update the 'requested' field
        exam_instance.requested = exam_serializer.validated_data['requested']
        exam_instance.save()

        # You might need to update the student serializer as well if needed
        serializer = self.get_serializer(instance)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
 

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('student_index')
    serializer_class = StudentSerializer

class StudentListView(APIView):
    def get(Self, request):
        all_student= Student.objects.all()
        serializers =StudentListSerializer(all_student,many = True)
        return Response(serializers.data)
    
class StudentListDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentListSerializer
    
class StudentDetailView(generics.RetrieveUpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentListSerializer

    def get(self, request, pk):
        instance = self.get_object()
        Single_student= Student.objects.get(pk= pk)
        serializer =StudentListSerializer(Single_student)
        return Response(serializer.data)
    
def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Assuming you have a serializer for ExamResult
        exam_serializer = ExamSerializer(data=request.data, partial=True)
        exam_serializer.is_valid(raise_exception=True)

        # Find the exam instance based on the provided 'id'
        exam_id = exam_serializer.validated_data['id']
        
        # Access the related set of exams for the specific student
        exam_instance = instance.Exams_Results.get(id=exam_id)

        # Update the 'requested' field
        exam_instance.requested = exam_serializer.validated_data['requested']
        exam_instance.save()

        # You might need to update the student serializer as well if needed
        serializer = self.get_serializer(instance)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)



@api_view(['GET'])
def ExamResults(request, pk):
    queryset = ExamResult.objects.get(student_index=pk)
    serializer_class = ExamSerializer(queryset)
    return Response(serializer_class.data)

class ExamList(generics.ListAPIView):
    serializer_class = ExamSerializer

    def get_queryset(self):
        return ExamResult.objects.filter(student_index=self.kwargs['student_index'])
    
class studentdetail(generics.RetrieveAPIView):
    def get(self,request, pk):
        queryset = Student.objects.get(student_index = pk)
        serializer_class = StudentListSerializer(queryset)
        lookup_field = 'student_index'

   

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

            return redirect('register')
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
            return redirect('DataEntry')

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
