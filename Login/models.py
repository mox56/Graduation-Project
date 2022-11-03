from random import choices
from django.db import models

# Create your models here.
class Department(models.Model):
    Code = models.CharField(max_length=10, null=True)
    name = models.CharField(max_length=100, null=True)    
    
    def __str__(self):
        return self.name

class Student(models.Model):
    index = models.IntegerField( null=True)
    name = models.CharField(max_length=100, null=True )
    Department = models.ManyToManyField(Department)
    Semester = models.IntegerField(null=True)   
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    
    
    def __str__(self):
        return self.name
    
class Course(models.Model):
    Code = models.CharField(max_length=10, null=True)
    Name =models.CharField(max_length=100, null=True)
    Department = models.ManyToManyField(Department)
    Semester = models.IntegerField(null=True)  
    CreditHours = models.IntegerField(null=True) 
    
    def __str__(self):
        return self.Name


    
class ExamResult(models.Model):
    STATUS = (
        ('A','A'), ('B','B'),('C','C'),('D','D'),('F','F'),('Z','Z')
    )
    student_index= models.ForeignKey(Student, null=True, on_delete= models.SET_NULL)
    Course_code= models.ForeignKey(Course, null=True, on_delete= models.SET_NULL)
    Mark=models.CharField( max_length=50, null=True, choices=STATUS)
    Semester= models.IntegerField(null=True) 
    
    def __str__(self):
        return self.Mark