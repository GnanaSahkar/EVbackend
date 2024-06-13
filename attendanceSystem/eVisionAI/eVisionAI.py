import cv2
import face_recognition
import numpy as np
import datetime
import os
import django
import sys

# Setup Django environment
project_path = 'D:/GnanaSahkar/eVisionBackend Model/attendanceSystem'
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendanceSystem.settings')
django.setup()

from attendance.models import Attendance, Intruder

class eVisionAI:
    def __init__(self, images_dir):
        self.images_dir = images_dir
        self.known_faces = []
        self.known_names = []
        self.attendance_marked = set()
        self.unknown_encodings = set()
        self.load_known_faces()

    def load_known_faces(self):
        for filename in os.listdir(self.images_dir):
            if filename.endswith(".jpg") or filename.endswith(".jpeg"):
                name = os.path.splitext(filename)[0]
                image_path = os.path.join(self.images_dir, filename)
                image = face_recognition.load_image_file(image_path)
                face_encoding = face_recognition.face_encodings(image)[0]
                self.known_faces.append(face_encoding)
                self.known_names.append(name)

    def process_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(self.known_faces, face_encoding)
            name = "Unknown"
            match_index = np.argwhere(matches)
            if match_index.size > 0:
                match_index = match_index[0][0]
                name = self.known_names[match_index]
                if name not in self.attendance_marked:
                    self.record_attendance(name, frame)
                    self.attendance_marked.add(name)
            else:
                if face_encoding.tobytes() not in self.unknown_encodings:
                    self.record_intruder(face_encoding, frame)
                    self.unknown_encodings.add(face_encoding.tobytes())

            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    def record_attendance(self, name, frame):
        timestamp = datetime.datetime.now()
        directory = "Attended_faces"
        if not os.path.exists(directory):
            os.makedirs(directory)
        image_path = os.path.join(directory, f"{name}.jpg")
        Attendance.objects.create(person_id=name, timestamp=timestamp, image_path=image_path)
        cv2.imwrite(image_path, frame)

    def record_intruder(self, face_encoding, frame):
        timestamp = datetime.datetime.now()
        directory = "unknown_faces"
        if not os.path.exists(directory):
            os.makedirs(directory)
        image_path = os.path.join(directory, f"intruder_{timestamp.strftime('%Y%m%d_%H%M%S')}.jpg")
        Intruder.objects.create(timestamp=timestamp)
        cv2.imwrite(image_path, frame)

    def start(self, video_source=0):
        cap = cv2.VideoCapture(video_source)
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Cannot read frame")
                break
            self.process_frame(frame)
            cv2.imshow("Face Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    eVisionAI_module = eVisionAI("D:/GnanaSahkar/eVisionBackend Model/attendanceSystem/eVisionAI/images")

    eVisionAI_module.start()
    print("eVisionAI has finished running.")