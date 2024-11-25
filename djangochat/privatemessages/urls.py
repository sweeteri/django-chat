from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('conversation/<int:user_id>/', views.conversation, name='conversation'),
]