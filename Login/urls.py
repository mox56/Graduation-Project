import imp
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path('', views.loginUser, name="login"),
    path('login/', views.loginUser, name="login"),
    path('cs/', views.ComputerScience, name="cs"),
    path('register', views.register, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('AddStudent/', views.AddStudent, name="AddStudent"),
    path('UpdateStudent/<str:pk>/', views.UpdateStudent, name="UpdateStudent"),
    path('DeleteStudent/<str:pk>/', views.DeleteStudent, name="DeleteStudent")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
