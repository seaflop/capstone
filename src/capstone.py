from tts import TTS
from ocr import OCR
import cv2
import file_locations as fl

class Capstone(TTS, OCR):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def take_picture(self, image_file_location: str):
        
        camera = cv2.VideoCapture(0)
        if (not camera.isOpened()):
            raise OSError("Error: Could not open the webcam")
        
        while True:
            # Capture frame-by-frame
            ret, frame = camera.read()

            if not ret:
                print("Error: Could not read frame.")
                break

            # Display the resulting frame
            cv2.imshow('Webcam Feed - Press s to Save, q to Quit', frame)

            # Wait for a key press
            key = cv2.waitKey(1) & 0xFF

            # If 's' is pressed, save the image
            if key & 0xFF == ord(" "):
                self.play(fl.camera_sound_path)
                image_name = image_file_location
                cv2.imwrite(image_name, frame)
                break
            
            # If 'q' is pressed, quit the application
            elif key & 0xFF == 27:
                break

        # When everything is done, release the capture and destroy windows
        camera.release()
        cv2.destroyAllWindows()