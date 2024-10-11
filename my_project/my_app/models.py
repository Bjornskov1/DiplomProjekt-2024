from django.db import models

class Meeting(models.Model):
    INITIAL_CHOICES = [
        ('AB', 'AB'),
        ('CD', 'CD'),
        ('EF', 'EF'),
        ('GH', 'GH'),
    ]

    name = models.CharField(max_length=100, choices=INITIAL_CHOICES)
    date = models.DateField()
    start_time = models.TimeField()  # Make sure this is present
    end_time = models.TimeField()    # Make sure this is present
    duration = models.CharField(max_length=20)
    notes = models.CharField(max_length=100, null=True)  # Temporary field