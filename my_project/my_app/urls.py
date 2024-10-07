from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book-meeting/', views.book_meeting, name='book_meeting'),
    path('view-meetings/', views.view_meetings, name='view_meetings'),
    path('clear-meetings/', views.clear_meetings, name='clear_meetings'),  # New route for clearing meetings
]
