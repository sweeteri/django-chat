from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from roomchat.models import Room
from channels.testing import WebsocketCommunicator
from djangochat.asgi import application


class RoomChatViewsTestCase(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client = Client()

        # Создаем комнату
        self.room = Room.objects.create(name="Test Room", slug="test-room", created_by=self.user)

    def test_rooms_page_access(self):
        # Проверка доступа к странице комнат
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse("rooms"))
        self.assertEqual(response.status_code, 200)

    def test_create_room(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('create_room'),
                                    {'name': 'Test Room'})  # Убедитесь, что ключи соответствуют вашим полям
        self.assertEqual(response.status_code, 302)  # Проверяем перенаправление
