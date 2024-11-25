from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/direct/<int:user_id>/', consumers.PersonalMessageConsumer.as_asgi()),
]