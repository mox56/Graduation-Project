from random import choices
from django.db import models
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):

        user = self.model(
            username=username,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("superuser has to have is_staff being true")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("superuser has to have is_superuser being true")

        return self.create_user(username=username, password=password, **extra_fields)


class User(AbstractUser):
    is_admin = models.BooleanField('is_admin', default=False)
    is_registrar = models.BooleanField('is_registrar', default=False)
    is_dataentry = models.BooleanField('is_dataentry', default=False)

    username = models.CharField(max_length=80, unique=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class Department(models.Model):
    VALUE = (('Computer Science', 'Computer Science'),
             ('Information Technology', 'Information Technology'))

    department_id = models.IntegerField(primary_key=True)
    Code = models.CharField(max_length=10, null=True)
    name = models.CharField(max_length=100, null=True, choices=VALUE)

    def __str__(self):
        return self.name


class Student(models.Model):

    student_index = models.IntegerField(
        primary_key=True, default="0")
    name = models.CharField(max_length=100, null=True)
    department = models.ForeignKey(
        Department, null=True, on_delete=models.CASCADE)
    Semester = models.IntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    password = models.IntegerField(default="0")

    def __str__(self):
        string = '{0}'.format(self.student_index)
        return string


class Course(models.Model):
    Code = models.CharField(max_length=10, primary_key=True,
                            unique=True)
    Name = models.CharField(max_length=100, null=True)
    Mark = models.CharField(max_length=50, null=True)
    
    def __str__(self):
        return self.Code
    


class ExamResult(models.Model):
    #id = models.IntegerField(primary_key= True, default = 0)

    student_index = models.ForeignKey(Student,on_delete = models.CASCADE,
         related_name="Exams_Results")
    
    Semester = models.IntegerField ( default = 1)
    
    Course_code = models.CharField(
        max_length = 10)
    
    Course_name = models.CharField(
        max_length = 50)
    
    Mark = models.CharField(max_length=50, null=True)

    Credit_hours = models.IntegerField(default = 2)

    requested = models.BooleanField(default = False)
    


def __str__(self):
    return self.Course_code
