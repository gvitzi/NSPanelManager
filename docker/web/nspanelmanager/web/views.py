from django.shortcuts import render, redirect

from .models import NSPanel, Room


def index(request):
    return render(request, 'index.html', {'nspanels': NSPanel.objects.all()})


def rooms(request):
    return render(request, 'rooms.html', {'rooms': Room.objects.all()})


def edit_room(request, room_id: int):
    return render(request, 'edit_room.html', {'room': Room.objects.filter(id=room_id).first()})


def save_new_room(request):
    new_room = Room()
    new_room.friendly_name = request.POST['friendly_name']
    new_room.save()
    return redirect('rooms')


def update_room_form(request, room_id: int):
    room = Room.objects.filter(id=room_id).first()
    room.friendly_name = request.POST['friendly_name']
    room.save()
    return redirect('edit_room', room_id=room_id)
