import cv2
import os
import logging
logging.basicConfig(level=logging.INFO, format = " %(asctime)s - %(levelname)s - %(message)s")
#logging.disable(logging.CRITICAL) # COMMENT OUT THIS LINE TO DISABLE LOGGING MESSAGES

os.environ["DISABLE_MODEL_SOURCE_CHECK"] = "True"
from paddleocr import PaddleOCR
#paddle.set_num_threads(2)

image_dir = "./images"
image_file = "example2.jpg"
image_path = os.path.join(image_dir, image_file)
base_image_file = "image.jpg"

ocr_dir = "./ocr"
ocr_file = "ocr1.txt"
ocr_path = os.path.join(ocr_dir, ocr_file)
base_ocr_path = "ocr.txt"

scaled_height = 1080

def resize_image(image_path: str):
    global scaled_height

    img = cv2.imread(image_path)
    height = img.shape[0]
    logging.info(f"height of the original image is {height}")

    scale_factor = round(scaled_height / height, 2) 
    logging.info(f"the factor to scale the image by is {scale_factor}")

    resized_image = cv2.resize(img, (0,0), fx = scale_factor, fy = scale_factor)
    logging.info(f"resized the image")

    # Remove the original image and keep only the new resized image in the same path
    os.remove(image_path)
    logging.info(f"removed the original image located at {image_path}")
    cv2.imwrite(image_path, resized_image)
    logging.info(f"created a new resized image located at {image_path}")

def ocr(image_path):
    ocr = PaddleOCR(
        lang='en'
    )

    result = ocr.predict(image_path)
    extracted_text = result[0]["rec_texts"]

    with open(ocr_path, "w") as f:
        for text in extracted_text:
            f.write(text + " ")

resize_image(image_path)
ocr(image_path)