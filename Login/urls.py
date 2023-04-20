from Login import views
from django.views.generic import RedirectView
import imp
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import RegisterAPI
from django.urls import include, path
from rest_framework import routers
from Login.models import *
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from knox import views as knox_views
from .views import LoginAPI




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
    path('DataEntry/', views.DataEntry, name="DataEntry"),
    path('Registrar/', views.Registrar, name="Registrar"),
    path('register', views.register, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('AddStudent/', views.AddStudent, name="AddStudent"),
    path('UpdateStudent/<str:pk>/', views.UpdateStudent, name="UpdateStudent"),
    path('DeleteStudent/<str:pk>/', views.DeleteStudent, name="DeleteStudent"),
    path('UpdateResult/<str:pk>/', views.UpdateResult, name="UpdateResult"),
    path('DeleteResult/<str:pk>/', views.DeleteResult, name="DeleteResult"),
    path('AddResult/', views.AddResult, name="AddResult"),
    path('api/register/', views.RegisterAPI.as_view(), name='register'),
    path('api/login/',views.LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns = format_suffix_patterns(urlpatterns)
