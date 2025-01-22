from django.http import HttpResponse
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Maps root URL to the home view
    path('home/', views.home, name='home_alt'),  # Allows access to home view via /home/
    path('book-meeting/', views.book_meeting, name='book_meeting'),
    path('clear-meetings/', views.clear_meetings, name='clear_meetings'),
    path('api/get-meetings/', views.get_meetings, name='get_meetings'),
    path('api/cleanup-meetings/', views.cleanup_meetings, name='cleanup_meetings'),

    #Møderum 1 og 2 with delete for main unit
    path('room/moderum_1/', views.view_meetings_for_room_1, name='view_meetings_room_1'),
    path('room/moderum_2/', views.view_meetings_for_room_2, name='view_meetings_room_2'),

    #Møderum 1 og 2 no buttons for subunits
    path('room/moderum_1/no-buttons/', views.view_meetings_for_room_1_no_buttons, name='view_meetings_room_1_no_buttons'),
    path('room/moderum_2/no-buttons/', views.view_meetings_for_room_2_no_buttons, name='view_meetings_room_2_no_buttons'),
    path('api/delete-meeting/<int:meeting_id>/', views.delete_meeting, name='delete_meeting'),
]
