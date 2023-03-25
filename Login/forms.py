from django import forms
from django.contrib.auth.forms import UserCreationForm

from django.forms import ModelForm
from .models import *
from rest_framework import serializers
from .models import User


class ExamForm(ModelForm):
    class Meta:
        model = ExamResult
        fields = '__all__'


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'user name',
                "class": "form-control"
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'password',
                "class": "form-control"
            }
        )
    )


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                "class": "fadeIn fourth"
            }
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter Passoword',
                "class": "fadeIn fourth"
            }
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter Password again',
                "class": "fadeIn fourth"
            }
        )
    )

    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Email',
                "class": "fadeIn fourth"
            }
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',
                  'is_admin', 'is_registrar', 'is_dataentry')
