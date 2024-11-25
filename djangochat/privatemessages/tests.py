from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from channels.testing import WebsocketCommunicator
from djangochat.asgi import application
from django.contrib.auth import get_user_model

class PrivateMessagesTestCase(TestCase):
    def setUp(self):
        # Создаем двух пользователей
        self.user1 = User.objects.create_user(username="user1", password="password1")
        self.user2 = User.objects.create_user(username="user2", password="password2")
        self.client = Client()

    def test_conversation_list_access(self):
        # Проверка доступа к списку пользователей
        self.client.login(username="user1", password="password1")
        response = self.client.get(reverse("user_list"))
        self.assertEqual(response.status_code, 200)

    def test_conversation_detail_access(self):
        # Проверка доступа к деталям переписки
        self.client.login(username="user1", password="password1")
        response = self.client.get(reverse("conversation", kwargs={"user_id": self.user2.id}))
        self.assertEqual(response.status_code, 200)

