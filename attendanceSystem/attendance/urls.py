from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('video_feed/', views.video_feed, name='video_feed'),
    path('upload_attendance/', views.upload_attendance, name='upload_attendance'),
    path('upload_intruder/', views.upload_intruder, name='upload_intruder'),
    path('attendance_report/', views.attendance_report, name='attendance_report'),
    path('intruder_report/', views.intruder_report, name='intruder_report'),
    
]