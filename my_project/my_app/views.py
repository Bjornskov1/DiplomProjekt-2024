from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Meeting
from datetime import datetime, timedelta


def home(request):
    return render(request, 'my_app/home.html')


def book_meeting(request):
    if request.method == 'POST':
        name = request.POST['name']
        date_str = request.POST['date']
        start_time_str = request.POST['start_time']
        duration = request.POST['duration']
        room = request.POST['room']  # Capture room selection

        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        start_time = datetime.strptime(start_time_str, '%H:%M').time()

        start_datetime = datetime.combine(date, start_time)

        if duration == '15 minutes':
            end_datetime = start_datetime + timedelta(minutes=15)
        elif duration == '30 minutes':
            end_datetime = start_datetime + timedelta(minutes=30)
        elif duration == '60 minutes':
            end_datetime = start_datetime + timedelta(minutes=60)
        else:
            end_datetime = start_datetime

        end_time = end_datetime.time()

        # Check for overlapping meetings in the same room
        overlapping_meetings = Meeting.objects.filter(
            date=date,
            start_time__lt=end_time,
            end_time__gt=start_time,
            room=room  # Only check for conflicts in the same room
        )

        if overlapping_meetings.exists():
            messages.error(request, 'This time slot is already taken in the selected room. Please choose a different time or room.')
            return render(request, 'my_app/booking.html')

        # Save the new meeting
        new_meeting = Meeting(name=name, date=date, start_time=start_time, end_time=end_time, duration=duration, room=room)
        new_meeting.save()

        messages.success(request, 'Meeting booked successfully!')
        return redirect('view_meetings')

    return render(request, 'my_app/booking.html')


def view_meetings(request):
    meetings = Meeting.objects.all()
    return render(request, 'my_app/view_meetings.html', {'meetings': meetings})


def clear_meetings(request):
    Meeting.objects.all().delete()  # Deletes all meetings
    return redirect('view_meetings')