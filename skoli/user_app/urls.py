from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('logga-in/', views.loginPage, name='login-page'),
    path('registrera-dig', views.registerPage, name='register-page'),
    path('logga-ut', views.logoutPage, name='logga-ut'),
    
    path('min-profil/', views.profilePage, name='profile-page'),
]
