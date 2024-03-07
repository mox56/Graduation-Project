from rest_framework import serializers
from Login.models import *
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.validators import ValidationError
from rest_framework.response import Response
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
    



class ExamSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required = False)
    class Meta:
        model = ExamResult
        exclude =['student_index']

        read_only_fields = ('Course_code','Course_name',"Mark", "id")     

    def create(self, validated_data):
        return ExamResult.objects.create(**validated_data)

    def update(self, instance, validated_data):
        
        instance.requested =validated_data.get('requested', instance.requested)
        

        instance.save()
        return instance
    
class StudentListSerializer(serializers.ModelSerializer):
    
    name = serializers.CharField()
    Exams_Results = ExamSerializer(many = True) 

    class Meta:
        model = Student
        exclude = ['department', 'Semester', 'password','date_created']

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

    #def update(self,instance, validated_data):
       # Exams_Results = validated_data.pop('Exams_Results')
        #instance.requested =validated_data.get("requested",instance.requested)
        #instance.save()
        #keep_Exams_Results = []
        #existing_ids =[e.id for e in instance.ExamS_Results]
        #for Exams_Result in Exams_Results:
        #    if "id" in Exams_Result.keys():
        #        if ExamResult.objects.filter(id = Exams_Result["id"]).exist():
        #            e= ExamResult.objects.get(id=ExamResult["id"])
       #             e.requested = Exams_Result.get('requested',e.requested)
        #            e.save()
        #            keep_Exams_Results.append(e.id)
        #        else:
        #            continue
        #    return instance     



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
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["username", "password"]

    def validate(self, attrs):
        username_exists = User.objects.filter(
            username=attrs['username']).exists()

        if username_exists:
            raise ValidationError("Username has already been used")
        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        Token.objects.create(user=user)
        return user
