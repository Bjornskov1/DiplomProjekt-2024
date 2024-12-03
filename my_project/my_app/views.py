import json
import logging

from datetime import datetime, timedelta

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Meeting, User
from .forms import MeetingForm
from django.db import models

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'my_app/home.html')


# Broadcast opdateringer, når møder ændres
def broadcast_meeting_update(room_name):
    group_name = room_name.replace(" ", "_").replace("ø", "o").lower()
    logger.info(f"Broadcasting update to group: {group_name}")  # Debug log

    # Fetch meetings
    today = datetime.now().date()
    meetings = Meeting.objects.filter(date__gte=today, room=room_name)

    events = [
        {
            "title": meeting.user.name,
            "start": f"{meeting.date}T{meeting.start_time}",
            "end": f"{meeting.date}T{meeting.end_time}",
            "description": f"Duration: {meeting.duration}"
        }
        for meeting in meetings
    ]

    # Broadcast to WebSocket group
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            "type": "meeting_update",
            "message": json.dumps(events)
        }
    )
    logger.info(f"Broadcast sent to group: {group_name}")  # Confirm broadcast

def book_meeting(request):
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            new_meeting = form.save(commit=False)

            # Valider og beregn slut-tidspunkt
            today = datetime.now().date()
            if new_meeting.date < today:
                messages.error(request, 'You cannot book a meeting for a past date.')
                return render(request, 'my_app/booking.html', {'form': form})

            start_datetime = datetime.combine(new_meeting.date, new_meeting.start_time)
            if new_meeting.duration == '15 minutes':
                end_datetime = start_datetime + timedelta(minutes=15)
            elif new_meeting.duration == '30 minutes':
                end_datetime = start_datetime + timedelta(minutes=30)
            elif new_meeting.duration == '60 minutes':
                end_datetime = start_datetime + timedelta(minutes=60)
            else:
                end_datetime = start_datetime  # Default for "Whole Day"

            new_meeting.end_time = end_datetime.time()

            overlapping_meetings = Meeting.objects.filter(
                date=new_meeting.date,
                start_time__lt=new_meeting.end_time,
                room=new_meeting.room
            )
            if overlapping_meetings.exists():
                messages.error(request, 'This time slot is already taken in the selected room.')
                return render(request, 'my_app/booking.html', {'form': form})

            # Gem mødet og broadcast opdateringer
            new_meeting.save()
            broadcast_meeting_update(new_meeting.room)
            messages.success(request, 'Meeting booked successfully!')
            return redirect('view_meetings')
    else:
        form = MeetingForm()
    users = User.objects.all()
    return render(request, 'my_app/booking.html', {'form': form, 'users': users})


def view_meetings(request):
    today = datetime.now().date()
    meetings = Meeting.objects.filter(date__gte=today)
    return render(request, 'my_app/view_meetings.html', {'meetings': meetings})


def cancel_meeting(request, name):
    try:
        meeting = Meeting.objects.get(name=name)
        room_name = meeting.room  # Gem rumnavnet inden sletning
        meeting.delete()
        broadcast_meeting_update(room_name)  # Broadcast opdateringer
        messages.success(request, 'Meeting cancelled successfully!')
    except Meeting.DoesNotExist:
        messages.error(request, 'Meeting not found.')
    return redirect('view_meetings')


def edit_meeting(request, name):
    meeting = get_object_or_404(Meeting, name=name)
    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            updated_meeting = form.save(commit=False)

            # Valider og beregn slut-tidspunkt
            start_datetime = datetime.combine(updated_meeting.date, updated_meeting.start_time)
            duration_mapping = {'15 minutes': 15, '30 minutes': 30, '60 minutes': 60}
            end_datetime = start_datetime + timedelta(minutes=duration_mapping.get(updated_meeting.duration, 0))
            updated_meeting.end_time = end_datetime.time()

            # Gem mødet og broadcast opdateringer
            updated_meeting.save()
            broadcast_meeting_update(updated_meeting.room)
            messages.success(request, 'Meeting updated successfully!')
            return redirect('view_meetings')
    else:
        form = MeetingForm(instance=meeting)
    users = User.objects.all()
    return render(request, 'my_app/edit_meeting.html', {'form': form, 'meeting': meeting, 'users': users})


def clear_meetings(request):
    Meeting.objects.all().delete()
    broadcast_meeting_update("Møderum 1")  # Broadcast opdateringer for begge rum
    broadcast_meeting_update("Møderum 2")
    messages.success(request, 'All meetings cleared.')
    return redirect('view_meetings')


def view_meetings_for_room_1(request):
    today = datetime.now().date()
    meetings = Meeting.objects.filter(date__gte=today, room="Møderum 1")
    events = [
        {
            "title": meeting.user.name,
            "start": f"{meeting.date}T{meeting.start_time}",
            "end": f"{meeting.date}T{meeting.end_time}",
            "description": f"Duration: {meeting.duration}"
        }
        for meeting in meetings
    ]
    return render(request, 'my_app/view_meetings_room.html', {
        'meetings': meetings,
        'room': 'Møderum 1',
        'events': events,
    })


def view_meetings_for_room_2(request):
    today = datetime.now().date()
    meetings = Meeting.objects.filter(date__gte=today, room="Møderum 2")
    events = [
        {
            "title": meeting.user.name,
            "start": f"{meeting.date}T{meeting.start_time}",
            "end": f"{meeting.date}T{meeting.end_time}",
            "description": f"Duration: {meeting.duration}"
        }
        for meeting in meetings
    ]
    return render(request, 'my_app/view_meetings_room.html', {
        'meetings': meetings,
        'room': 'Møderum 2',
        'events': events,
    })


def get_meetings(request):
    # Få rumnavnet fra forespørgselsparametrene
    room = request.GET.get('room', None)

    # Nu
    now = datetime.now()

    # Filtrér kommende møder baseret på dato, tid og rum
    if room:
        # Filtrér møder, der ikke er overståede
        meetings = Meeting.objects.filter(
            date__gte=now.date(),  # Dagens eller fremtidige møder
        ).filter(
            models.Q(date__gt=now.date()) | models.Q(start_time__gte=now.time()),  # Ikke overstået
            room=room
        ).order_by('date', 'start_time')
    else:
        meetings = Meeting.objects.filter(
            date__gte=now.date(),
        ).filter(
            models.Q(date__gt=now.date()) | models.Q(start_time__gte=now.time())
        ).order_by('date', 'start_time')

    return JsonResponse(list(meetings.values(
        'user__name', 'date', 'start_time', 'end_time', 'duration', 'room'
    )), safe=False)