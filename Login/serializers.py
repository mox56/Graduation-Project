from rest_framework import serializers
from Login.models import *
from django.contrib.auth.models import User


class StudentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        required=False, allow_blank=True, max_length=100)
    department = serializers.CharField(
        required=False, allow_blank=True, max_length=100)
    Semester = serializers.IntegerField(read_only=True)
    CGPA = serializers.FloatField(read_only=True)
    GPA = serializers.FloatField(read_only=True)

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


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', ]

    # def create(self, validated_data):
        # return Student.objects.create(validated_data)

    # def update(self, instance, validated_data):

     #   instance.name = validated_data.get('name', instance.title)
      #  instance.save()
       # return instance#\
