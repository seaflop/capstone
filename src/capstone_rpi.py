from tts import TTS
from ocr import OCR
from picamera2 import Picamera2

class Capstone(TTS, OCR):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def take_picture(self, image_file_location: str):
        camera = Picamera2()
        camera.start()
        camera.capture_file(image_file_location)
        camera.stop()