import django_filters

from .models import *


class SemesterFilter(django_filters.FilterSet):
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['student_index', 'name',
                   'department', 'date_created', 'CGPA', 'GPA']
