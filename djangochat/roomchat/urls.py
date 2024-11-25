from django.urls import path

from . import views

urlpatterns = [
    path('create-room/', views.create_room, name='create_room'),
    path('', views.rooms, name='rooms'),
    path('<slug:slug>/', views.room, name='room'),

]