from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('register/',views.register,name='register'),
    path('followers/',views.followers,name='followers'),
    path('following/',views.following,name='following'),
    path('recommended_users/',views.recommended_users,name='recommended_users'),
    path('analysis/',views.analysis,name='analysis'),
    path('add_post',views.add_post,name='add_post'),
]

