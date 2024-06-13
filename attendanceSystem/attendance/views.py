from django.shortcuts import render
from .models import Attendance
import os
from django.conf import settings
import datetime
from django.shortcuts import render
from django.http import StreamingHttpResponse
import threading
import cv2
import time
from django.http import JsonResponse
from attendance.models import Intruder




class VideoCamera:
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.lock = threading.Lock()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        with self.lock:
            ret, frame = self.video.read()
            if not ret:
                return None
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()

def gen(camera):
    while True:
        frame = camera.get_frame()
        if frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        time.sleep(1/30)  # Maintain a frame rate of about 30 FPS

def video_feed(request):
    return StreamingHttpResponse(gen(VideoCamera()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')

def home(request):
    return render(request, 'attendance/index.html')




def upload_attendance(request):
    # Your logic for handling the attendance upload
    return JsonResponse({'message': 'Attendance uploaded successfully'})
def upload_intruder(request):
    # Your logic for handling the upload of intruder data
    return JsonResponse({'message': 'Intruder data uploaded successfully'})

def get_attendance(request):
    # Your logic for retrieving attendance data
    # For example, querying the database for attendance records
    attendance_data = {'example_key': 'example_value'}  # Replace this with your actual data
    return JsonResponse(attendance_data)


def attendance_report(request):
    attendance_data = []
    images_dir = os.path.join(settings.BASE_DIR, 'attendanceSystem', 'eVisionAI', 'Attended_faces')
    
    for attendance_record in Attendance.objects.all():
        # Replace backslashes with forward slashes in the image path
        corrected_image_path = attendance_record.image_path.replace('\\', '/')
        
        # Build the image path
        image_path = os.path.join(images_dir, corrected_image_path)
        image_name = os.path.basename(image_path)
        name = os.path.splitext(image_name)[0]
        
        # Create the corrected URL for the image
        media_image_url = '/attendanceSystem/eVisionAI/' + corrected_image_path
        attendance_data.append({'name': name, 'timestamp': attendance_record.timestamp, 'image_path': media_image_url})
    
    return render(request, 'attendance/attendance_report.html', {'attendance_data': attendance_data})


def intruder_report(request):
    intruder_data = []
    for intruder_record in Intruder.objects.all():
        media_image_url = intruder_record.image_path.replace(os.path.join('eVisionAI', ''), '')
        intruder_data.append({'timestamp': intruder_record.timestamp, 'image_path': media_image_url})

    return render(request, 'attendance/intruder_report.html', {'intruder_data': intruder_data})