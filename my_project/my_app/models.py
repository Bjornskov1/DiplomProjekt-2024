from django.db import models

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.name} ({self.email})"

class Meeting(models.Model):
    ROOM_CHOICES = [
        ('Møderum 1', 'Møderum 1'),
        ('Møderum 2', 'Møderum 2'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="meetings", null=True)  # Allow null values temporarily
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration = models.CharField(max_length=20)
    room = models.CharField(max_length=20, choices=ROOM_CHOICES)

    def __str__(self):
        return f"Meeting with {self.user.name} on {self.date} at {self.start_time} in {self.room}"
