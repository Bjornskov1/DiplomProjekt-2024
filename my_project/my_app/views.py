import json
import logging

from datetime import datetime, timedelta
from asgiref.sync import async_to_sync
from celery.utils.time import make_aware
from channels.layers import get_channel_layer
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.utils.timezone import localtime
from .utils import send_email_via_graph_api
from datetime import timedelta
from django.utils.timezone import make_aware
from .models import Meeting, User
from .forms import MeetingForm
from django.db import models

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'my_app/home.html')


# Broadcast updates to WebSocket group
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
        users = User.objects.all()
        if form.is_valid():
            new_meeting = form.save(commit=False)

            current_time = now()  # Current time with timezone awareness
            buffer_time = current_time - timedelta(minutes=1)  # Allow up to 1 minute buffer

            # Validate past date
            if new_meeting.date < current_time.date():
                messages.error(request, 'You cannot book a meeting for a past date.')
                return render(request, 'my_app/booking.html', {'form': form, 'users': users})


            start_datetime = make_aware(datetime.combine(new_meeting.date, new_meeting.start_time))

            # Validate same-day past time with a 1-minute buffer for "now" time
            if new_meeting.date == current_time.date() and start_datetime < buffer_time:
                messages.error(request, 'You cannot book a meeting for a time more than 1 minute in the past.')
                return render(request, 'my_app/booking.html', {'form': form, 'users': users})

            # Calculate end time
            if new_meeting.duration == '15 minutes':
                end_datetime = start_datetime + timedelta(minutes=15)
            elif new_meeting.duration == '30 minutes':
                end_datetime = start_datetime + timedelta(minutes=30)
            elif new_meeting.duration == '60 minutes':
                end_datetime = start_datetime + timedelta(minutes=60)
            elif new_meeting.duration == '120 minutes':
                end_datetime = start_datetime + timedelta(minutes=120)
            else:
                end_datetime = start_datetime

            new_meeting.end_time = end_datetime.time()

            # Validate overlapping meetings
            overlapping_meetings = Meeting.objects.filter(
                date=new_meeting.date,
                start_time__lt=new_meeting.end_time,
                end_time__gt=new_meeting.start_time,
                room=new_meeting.room
            )
            if overlapping_meetings.exists():
                messages.error(request, 'This time slot is already taken in the selected room.')
                return render(request, 'my_app/booking.html', {'form': form, 'users': users})

            # Save meeting and broadcast
            new_meeting.save()
            broadcast_meeting_update(new_meeting.room)
            messages.success(request, 'Meeting booked successfully and Mail is sent!')

            # Send email to user
            subject = f"Meeting Confirmation: {new_meeting.room}"
            body = (f"Dear {new_meeting.user.name},\n\n"
                    f"Your meeting has been successfully booked. \n"
                    f"Details: \n"
                    f"Room: {new_meeting.room}\n"
                    f"Date: {new_meeting.date}\n"
                    f"Time: {new_meeting.start_time} - {new_meeting.end_time}\n"
                    f"Duration: {new_meeting.duration}\n\n"
                    f"Thank you.")
            send_email_via_graph_api(new_meeting.user.email, subject, body)

            # Render the form again to stay on the page
            form = MeetingForm()
            return render(request, 'my_app/booking.html', {'form': form, 'users': users})

        else:
            messages.error(request, 'Invalid form submission. Please check your inputs.')
    else:
        form = MeetingForm()
        users = User.objects.all()

    return render(request, 'my_app/booking.html', {'form': form, 'users': users})


def view_meetings(request):
    today = datetime.now().date()
    meetings = Meeting.objects.filter(date__gte=today)
    return render(request, 'my_app/view_meetings.html', {'meetings': meetings})


def cancel_meeting(request, name): #Older version
    try:
        meeting = Meeting.objects.get(name=name)
        room_name = meeting.room
        meeting.delete()
        broadcast_meeting_update(room_name)
        messages.success(request, 'Meeting cancelled successfully!')
    except Meeting.DoesNotExist:
        messages.error(request, 'Meeting not found.')
    return redirect('view_meetings')


def clear_meetings(request): #Older version
    Meeting.objects.all().delete()
    broadcast_meeting_update("Møderum 1")
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
def view_meetings_for_room_1_no_buttons(request):
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
    return render(request, 'my_app/view_meetings_room_no_buttons.html', {
        'meetings': meetings,
        'room': 'Møderum 1',
        'events': events,
    })


def view_meetings_for_room_2_no_buttons(request):
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
    return render(request, 'my_app/view_meetings_room_no_buttons.html', {
        'meetings': meetings,
        'room': 'Møderum 2',
        'events': events,
    })


def get_meetings(request):
    room = request.GET.get('room', None)
    current_time = now()

    if room:
        meetings = Meeting.objects.filter(
            date__gte=current_time.date(),  # Today's or future dates
            room=room
        ).filter(
            models.Q(date__gt=current_time.date()) |  # Future meetings
            models.Q(start_time__lte=current_time.time(), end_time__gte=current_time.time()) |  # Ongoing meetings
            models.Q(start_time__gte=current_time.time())  # Future meetings today
        ).order_by('date', 'start_time')
    else:
        meetings = Meeting.objects.filter(
            date__gte=current_time.date(),
        ).filter(
            models.Q(date__gt=current_time.date()) |
            models.Q(start_time__lte=current_time.time(), end_time__gte=current_time.time()) |
            models.Q(start_time__gte=current_time.time())
        ).order_by('date', 'start_time')

    return JsonResponse(list(meetings.values(
        'id', 'user__name', 'date', 'start_time', 'end_time', 'duration', 'room'
    )), safe=False)

def cleanup_meetings(request):
    current_time = localtime()  # Use timezone-aware local time

    # Identify past meetings
    past_meetings = Meeting.objects.filter(
        models.Q(date__lt=current_time.date()) |  # Meetings before today
        models.Q(date=current_time.date(), end_time__lte=current_time.time())  # Meetings today but already ended
    )
    #print(f"Current time: {current_time.time()}")
    #print(past_meetings)


    logger.info(f"Meetings to delete: {[meeting.id for meeting in past_meetings]}")

    # Count and delete past meetings for debug
    count = past_meetings.count()
    room_names = past_meetings.values_list('room', flat=True).distinct()
    past_meetings.delete()

    # Broadcast updates for each room
    for room_name in room_names:
        broadcast_meeting_update(room_name)

    return JsonResponse({'deleted_count': count})


def delete_meeting(request, meeting_id):
    if request.method == 'DELETE':
        try:
            # Fetch the meeting by ID
            meeting = get_object_or_404(Meeting, id=meeting_id)
            room_name = meeting.room
            meeting.delete()

            # Optionally broadcast an update to refresh data
            broadcast_meeting_update(room_name)

            return JsonResponse({'message': 'Meeting deleted successfully.'}, status=200)
        except Meeting.DoesNotExist:
            return JsonResponse({'error': 'Meeting not found.'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
