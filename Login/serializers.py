from rest_framework import serializers
from Login.models import *
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.validators import ValidationError
User = get_user_model()

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

    def create(self, validated_data):

        return Student.objects.create(**validated_data)

    def update(self, instance, validated_data):

        instance.name = validated_data.get('name', instance.name)
        instance.department = validated_data.get(
            'department', instance.department)
        instance.Semester = validated_data.get('Semester', instance.Semester)
        instance.CGPA = validated_data.get('CGPA', instance.CGPA)
        instance.GPA = validated_data.get('GPA', instance.GPA)

        instance.save()
        return instance


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
    extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password= serializers.CharField(min_length=8, write_only=True)
    class Meta:
        model = User
        fields = ["username", "password"]
        
    def validate(self, attrs):
        username_exists = User.objects.filter(username=attrs['username']).exists()

        if username_exists:
            raise ValidationError("Username has already been used")
        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user=super().create(validated_data)
        user.set_password(password)
        user.save()
        
        Token.objects.create(user=user)
        return user
