from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='start_time',
            field=models.TimeField(default='00:00'),  # Adjust the default if needed
        ),
        migrations.AddField(
            model_name='meeting',
            name='end_time',
            field=models.TimeField(default='00:00'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='notes',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
