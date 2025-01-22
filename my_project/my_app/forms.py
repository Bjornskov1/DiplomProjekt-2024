# my_app/forms.py
from django import forms
from .models import Meeting, User

class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['user', 'date', 'start_time', 'duration', 'room']

    def __init__(self, *args, **kwargs):
        super(MeetingForm, self).__init__(*args, **kwargs)
        # Set the queryset to all users in the User model
        self.fields['user'].queryset = User.objects.all()
