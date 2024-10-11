from django.db import models

class Meeting(models.Model):
    INITIAL_CHOICES = [
        ('AB', 'AB'),
        ('CD', 'CD'),
        ('EF', 'EF'),
        ('GH', 'GH'),
    ]

    ROOM_CHOICES = [
        ('Møderum 1', 'Møderum 1'),
        ('Møderum 2', 'Møderum 2'),
    ]

    name = models.CharField(max_length=100, choices=INITIAL_CHOICES, primary_key=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration = models.CharField(max_length=20)
    room = models.CharField(max_length=20, choices=ROOM_CHOICES)  # Ensure this exists in the model

    def __str__(self):
        return f'{self.name} on {self.date} at {self.start_time} in {self.room}'