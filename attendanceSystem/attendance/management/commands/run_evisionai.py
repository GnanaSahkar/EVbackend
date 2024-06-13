from django.core.management.base import BaseCommand
from eVisionAI.eVisionAI import eVisionAI  # Adjust the import based on the actual path

class Command(BaseCommand):
    help = 'Run eVisionAI'

    def handle(self, *args, **kwargs):
        images_dir = "D:/GnanaSahkar/eVisionBackend Model/attendanceSystem/eVisionAI/images"
        eVisionAI_module = eVisionAI(images_dir)
        eVisionAI_module.start()
