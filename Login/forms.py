from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ("username", "email", "password", "password")

    username = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'placeholder': 'Username', 'class': 'fadeIn second'}))
    email = forms.CharField(max_length=100, widget=forms.EmailInput(
        attrs={'placeholder': 'Email', 'class': 'fadeIn third'}))
    password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(
        attrs={'placeholder': 'Password', 'class': 'fadeIn fourth'}))
    password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(
        attrs={'placeholder': 'Re-enter Password', 'class': 'fadeIn fourth'}))


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
