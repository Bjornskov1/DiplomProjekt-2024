from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Maps root URL to the home view
    path('home/', views.home, name='home_alt'),  # Allows access to home view via /home/
    path('book-meeting/', views.book_meeting, name='book_meeting'),
    path('view-meetings/', views.view_meetings, name='view_meetings'),
    path('cancel-meeting/<str:name>/', views.cancel_meeting, name='cancel_meeting'),
    path('edit-meeting/<str:name>/', views.edit_meeting, name='edit_meeting'),
    path('clear-meetings/', views.clear_meetings, name='clear_meetings'),
]
