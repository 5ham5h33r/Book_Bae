
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('searchres/', views.searchres, name='searchres'),
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutpage, name='logout'),
    path('register/', views.register, name='register'),
    path('updateshelf/', views.updateshelf, name='updateshelf'),
    path('bookshelf/', views.bookshelf, name='bookshelf'),
    path('removebook/<str:id>', views.removebook, name='removebook')



]
