from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Meeting, User
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from .forms import MeetingForm

def home(request):
    return render(request, 'my_app/home.html')


def book_meeting(request):
    if request.method == 'POST':
        # Initialize the form with POST data
        form = MeetingForm(request.POST)

        # Check if form data is valid
        if form.is_valid():
            # Save the meeting instance
            new_meeting = form.save(commit=False)  # Get the instance without saving yet

            # Check if the selected date is in the past
            today = datetime.now().date()
            if new_meeting.date < today:
                messages.error(request, 'You cannot book a meeting for a past date.')
                return render(request, 'my_app/booking.html', {'form': form})

            # Calculate the end time based on duration
            start_datetime = datetime.combine(new_meeting.date, new_meeting.start_time)
            if new_meeting.duration == '15 minutes':
                end_datetime = start_datetime + timedelta(minutes=15)
            elif new_meeting.duration == '30 minutes':
                end_datetime = start_datetime + timedelta(minutes=30)
            elif new_meeting.duration == '60 minutes':
                end_datetime = start_datetime + timedelta(minutes=60)
            else:
                end_datetime = start_datetime  # Default end time for "Whole Day"

            new_meeting.end_time = end_datetime.time()

            # Check for overlapping meetings in the same room
            overlapping_meetings = Meeting.objects.filter(
                date=new_meeting.date,
                start_time__lt=new_meeting.end_time,
                room=new_meeting.room
            )

            if overlapping_meetings.exists():
                messages.error(
                    request,
                    'This time slot is already taken in the selected room. Please choose a different time or room.'
                )
                return render(request, 'my_app/booking.html', {'form': form})

            # Save the new meeting to the database
            new_meeting.save()
            messages.success(request, 'Meeting booked successfully!')
            return redirect('view_meetings')
    else:
        # If GET request, create an empty form
        form = MeetingForm()

    # Fetch users from the database and pass to the template
    users = User.objects.all()
    return render(request, 'my_app/booking.html', {'form': form, 'users': users})


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


from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import Meeting, User
from .forms import MeetingForm

def edit_meeting(request, name):
    # Retrieve the meeting using the unique name
    meeting = get_object_or_404(Meeting, name=name)
    users = User.objects.all()  # Fetch all users for the dropdown list

    if request.method == 'POST':
        # Bind form with POST data to update meeting details
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            # Save the updated meeting
            updated_meeting = form.save(commit=False)

            # Calculate the end time based on duration, similar to booking
            start_datetime = datetime.combine(updated_meeting.date, updated_meeting.start_time)
            duration_mapping = {'15 minutes': 15, '30 minutes': 30, '60 minutes': 60}
            end_datetime = start_datetime + timedelta(minutes=duration_mapping.get(updated_meeting.duration, 0))
            updated_meeting.end_time = end_datetime.time()

            updated_meeting.save()  # Save changes to the database
            messages.success(request, 'Meeting updated successfully!')
            return redirect('view_meetings')
    else:
        # Populate form with the existing meeting instance for GET requests
        form = MeetingForm(instance=meeting)

    return render(request, 'my_app/edit_meeting.html', {
        'form': form,
        'meeting': meeting,
        'users': users  # Pass users to the template for user selection
    })



def clear_meetings(request):
    Meeting.objects.all().delete()
    messages.success(request, 'All meetings cleared.')
    return redirect('view_meetings')
