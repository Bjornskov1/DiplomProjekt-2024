from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Meeting
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404

def home(request):
    return render(request, 'my_app/home.html')


def book_meeting(request):
    if request.method == 'POST':
        name = request.POST['name']
        date_str = request.POST['date']
        start_time_str = request.POST['start_time']
        duration = request.POST['duration']
        room = request.POST['room']

        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        start_time = datetime.strptime(start_time_str, '%H:%M').time()

        # Check if the selected date is in the past
        today = datetime.now().date()
        if date < today:
            messages.error(request, 'You cannot book a meeting for a past date.')
            return render(request, 'my_app/booking.html')

        start_datetime = datetime.combine(date, start_time)

        # Calculate end time based on duration
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
            room=room
        )

        if overlapping_meetings.exists():
            messages.error(request,
                           'This time slot is already taken in the selected room. Please choose a different time or room.')
            return render(request, 'my_app/booking.html')

        # Save the new meeting
        new_meeting = Meeting(name=name, date=date, start_time=start_time, end_time=end_time, duration=duration,
                              room=room)
        new_meeting.save()

        messages.success(request, 'Meeting booked successfully!')
        return redirect('view_meetings')

    return render(request, 'my_app/booking.html')


def view_meetings(request):
    today = datetime.now().date()
    # Only show meetings today or in the future
    meetings = Meeting.objects.filter(date__gte=today)
    return render(request, 'my_app/view_meetings.html', {'meetings': meetings})


def cancel_meeting(request, name):
    try:
        # Fetch the meeting by 'name' since it's the primary key
        meeting = Meeting.objects.get(name=name)
        meeting.delete()
        messages.success(request, 'Meeting cancelled successfully!')
    except Meeting.DoesNotExist:
        messages.error(request, 'Meeting not found.')

    return redirect('view_meetings')


def edit_meeting(request, name):
    # Fetch the meeting using the 'name' field as the primary key
    meeting = get_object_or_404(Meeting, name=name)

    if request.method == 'POST':
        # Update meeting details with the form data
        meeting.date = request.POST['date']
        meeting.start_time = request.POST['start_time']
        meeting.duration = request.POST['duration']
        meeting.room = request.POST['room']
        meeting.save()

        messages.success(request, 'Meeting updated successfully!')
        return redirect('view_meetings')  # Redirect after successfully saving

    # Render the form with the existing meeting data pre-filled
    return render(request, 'my_app/edit_meeting.html', {'meeting': meeting})


def clear_meetings(request):
    Meeting.objects.all().delete()
    messages.success(request, 'All meetings cleared.')
    return redirect('view_meetings')
