from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('login/',views.loginPage, name='login'),
    path('signup/',views.signupPage, name='signup'),
    path('logout/',views.logoutUser, name='logout'),
    path('', views.home,name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('form/', views.createform, name='create-form'),
    path('update-form/<str:pk>/', views.updateform, name='update-form'),
    path('delete-room/<str:pk>/', views.deleteroom, name='delete-room'),
    path('deletemessage/<str:pk>/', views.deletemessage, name='deletemssg'),
    path('userprofile/<str:pk>/', views.UserProfile, name='user-profile'),
    path('updateprofile/<str:pk>/', views.updateProfile, name='update-profile'),
    path('topics/', views.Topics, name='topics'),
]