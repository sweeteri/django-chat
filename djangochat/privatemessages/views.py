# privatemessages/views.py

from django.shortcuts import render
from django.contrib.auth.models import User
from .models import DirectMessage

def user_list(request):
    users = User.objects.exclude(id=request.user.id)  # Исключаем текущего пользователя из списка
    return render(request, 'privatemessages/user_list.html', {'users': users})
def conversation(request, user_id):
    recipient = User.objects.get(id=user_id)
    messages = DirectMessage.objects.filter(
        sender=request.user, recipient=recipient
    ) | DirectMessage.objects.filter(
        sender=recipient, recipient=request.user
    )
    messages = messages.order_by('date_added')

    return render(request, 'privatemessages/conversation.html', {
        'recipient': recipient,
        'messages': messages,
    })

