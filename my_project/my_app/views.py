from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Meeting
from datetime import datetime, timedelta


def home(request):
    return render(request, 'my_app/home.html')


def book_meeting(request):
    if request.method == 'POST':
        # Now name refers to selected initials from the dropdown
        name = request.POST['name']
        date_str = request.POST['date']  # The date is coming as a string
        start_time_str = request.POST['start_time']  # The time is coming as a string
        duration = request.POST['duration']

        # Convert date and start_time strings to date and time objects
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        start_time = datetime.strptime(start_time_str, '%H:%M').time()

        # Calculate the end time based on duration
        start_datetime = datetime.combine(date, start_time)

        if duration == '15 minutes':
            end_datetime = start_datetime + timedelta(minutes=15)
        elif duration == '30 minutes':
            end_datetime = start_datetime + timedelta(minutes=30)
        elif duration == '60 minutes':
            end_datetime = start_datetime + timedelta(minutes=60)
        else:
            end_datetime = start_datetime  # If whole day or invalid, assume no end time

        end_time = end_datetime.time()

        # Check for overlapping meetings
        overlapping_meetings = Meeting.objects.filter(
            date=date,
            start_time__lt=end_time,
            end_time__gt=start_time
        )

        if overlapping_meetings.exists():
            # Add an error message to prompt the user
            messages.error(request, 'This time slot is already taken. Please choose a different time.')
            return render(request, 'my_app/booking.html')

        # Save the new meeting
        new_meeting = Meeting(name=name, date=date, start_time=start_time, end_time=end_time, duration=duration)
        new_meeting.save()

        # Show a success message when a meeting is successfully booked
        messages.success(request, 'Meeting booked successfully!')
        return redirect('view_meetings')

    return render(request, 'my_app/booking.html')


def view_meetings(request):
    meetings = Meeting.objects.all()
    return render(request, 'my_app/view_meetings.html', {'meetings': meetings})


def clear_meetings(request):
    Meeting.objects.all().delete()  # Deletes all meetings
    return redirect('view_meetings')
