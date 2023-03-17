from Login import views
from django.views.generic import RedirectView
import imp
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from django.urls import include, path
from rest_framework import routers
from Login.models import *
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets


router = routers.DefaultRouter()
router.include_format_suffixes = False
router.register(r'users', views.UserViewSet)
router.register(r'students', views.StudentViewSet)

urlpatterns = [


    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('students/', views.getStudent),
    path('students/<int:pk>/', views.StudentDetail),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', views.loginUser, name="login"),
    path('login/', views.loginUser, name="login"),
    path('cs/', views.ComputerScience, name="cs"),
    path('register', views.register, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('AddStudent/', views.AddStudent, name="AddStudent"),
    path('UpdateStudent/<str:pk>/', views.UpdateStudent, name="UpdateStudent"),
    path('DeleteStudent/<str:pk>/', views.DeleteStudent, name="DeleteStudent")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns = format_suffix_patterns(urlpatterns)
