# streaming/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('video_feed/', views.stream_video, name='stream_video'),
]
