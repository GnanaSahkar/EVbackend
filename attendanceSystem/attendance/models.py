from django.db import models

class Attendance(models.Model):
    person_id = models.CharField(max_length=50)
    timestamp = models.DateTimeField()
    image_path = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.person_id} - {self.timestamp}'

class Intruder(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    image_path = models.CharField(max_length=255)

    def __str__(self):
        return f'Intruder at {self.timestamp}'