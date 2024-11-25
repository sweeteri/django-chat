from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Room, Message
from .forms import RoomForm
@login_required
def rooms(request):
    rooms = Room.objects.all()

    return render(request, 'roomchat/rooms.html', {'rooms': rooms})

@login_required
def room(request, slug):
    room = get_object_or_404(Room, slug=slug)
    messages = Message.objects.filter(room=room)[0:25]

    return render(request, 'roomchat/room.html', {'room': room, 'messages': messages})
@login_required
def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.created_by = request.user
            room.save()
            return redirect('rooms')
    else:
        form = RoomForm()
    return render(request, 'roomchat/create_room.html', {'form': form})