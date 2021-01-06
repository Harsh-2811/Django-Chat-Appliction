from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('',views.index,name="home"),
    path('FirstApp/<str:room_name>/', views.room, name='room'),
    path('chat/',views.chats,name="char"),
    path('login/',views.loginprocess,name="login"),
    path('register/',views.register,name='register'),
    path('logout/',views.logoutProcesss,name='logot'),
    path('create_room/',views.create_room,name='create_room'),

    
]