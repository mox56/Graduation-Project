from random import choices
from django.db import models
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

# Create your models here.


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
        primary_key=True, default="0", verbose_name='student_index')
    name = models.CharField(max_length=100, null=True)
    department = models.ForeignKey(
        Department, null=True, on_delete=models.CASCADE)
    Semester = models.IntegerField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    CGPA = models.FloatField(null=True)
    GPA = models.FloatField(null=True)

    def __str__(self):
        string = '{0}  {1}   '.format(self.student_index, self.name)
        return string


class Course(models.Model):
    Code = models.CharField(max_length=10, primary_key=True,
                            verbose_name='Code', unique=True)
    Name = models.CharField(max_length=100, null=True)
    department = models.ForeignKey(
        Department, null=True, on_delete=models.CASCADE)
    Semester = models.IntegerField(null=True)
    CreditHours = models.IntegerField(null=True)

    def __str__(self):
        return self.Code


class ExamResult(models.Model):
    STATUS = (
        ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('F', 'F'), ('Z', 'Z')
    )
    student_index = models.ForeignKey(
        Student, to_field='student_index', on_delete=models.PROTECT)
    Course_code = models.ForeignKey(
        Course, to_field='Code', on_delete=models.CASCADE)
    Mark = models.CharField(max_length=50, null=True, choices=STATUS)
    Semester = models.CharField(max_length=30, null=True)
    department = models.ForeignKey(
        Department, null=True, on_delete=models.CASCADE)


def __str__(self):
    return self.student_index
