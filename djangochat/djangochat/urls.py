from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('chat.urls')),
    path('rooms/', include('roomchat.urls')),
path('privatemessages/', include('privatemessages.urls')),
    path('admin/', admin.site.urls),
]
