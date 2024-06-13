from django.apps import AppConfig
import threading
from django.core.management import call_command

class AttendanceConfig(AppConfig):
    name = 'attendance'

    def ready(self):
        threading.Thread(target=call_command, args=('run_evisionai',)).start()
