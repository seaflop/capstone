import cv2
import os
import logging
from rapidocr import RapidOCR 
logging.basicConfig(level=logging.INFO, format = " %(asctime)s - %(levelname)s - %(message)s")
logging.disable(logging.CRITICAL) # COMMENT OUT THIS LINE TO ENABLE LOGGING MESSAGES

class OCR():
    def __init__(self, scaled_image_height = 1080):
        self._scaled_image_height = scaled_image_height

    # Getter and setter methods for scaled_image_height
    @property
    def scaled_image_height(self):
        return self._scaled_image_height

    @scaled_image_height.setter
    def scaled_image_height(self, scaled_image_height: int):
        # Make sure that sclaed_image_height is an integer
        assert isinstance(scaled_image_height, int), "scaled_image_height must be an integer"

        self._scaled_image_height = scaled_image_height
    
    def ocr(self, image_file_location: str, text_file_location: str):
        engine = RapidOCR()

        result = engine(image_file_location)
        extracted_text = result.txts

        with open(text_file_location, "w") as f:
            for text in extracted_text:
                f.write(text + " ")

    def resize_image(self, image_location: str):
        img = cv2.imread(image_location)
        height = img.shape[0]
        logging.info(f"height of the original image is {height}")

        scale_factor = round(self._scaled_image_height / height, 2) 
        logging.info(f"the factor to scale the image by is {scale_factor}")

        resized_image = cv2.resize(img, (0,0), fx = scale_factor, fy = scale_factor)
        logging.info(f"resized the image")

        # Remove the original image and keep only the new resized image in the same path
        os.remove(image_location)
        logging.info(f"removed the original image located at {image_location}")
        cv2.imwrite(image_location, resized_image)
        logging.info(f"created a new resized image located at {image_location}")