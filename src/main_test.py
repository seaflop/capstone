import sys
# Assert Python version >= 3.10
MIN_VERSION = (3, 10)
if sys.version_info < MIN_VERSION:
    raise EnvironmentError(f"This script requires Python version {MIN_VERSION[0]}.{MIN_VERSION[1]} or higher.\nYou are using Python version {sys.version_info.major}.{sys.version_info.minor}")

import file_locations as fl
    
import argparse
# Define CLI arguments
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("-w", "--webcam", action="store_true", help="-w or --webcam takes an image with your webcam")
group.add_argument("-i", "--image", help="relative path of image file location")
args = parser.parse_args()


from capstone import Capstone

from pynput import keyboard
import time
import os
from threading import Thread

"""
    This function checks for key presses.
    It is used as part of the keyboard.Listener() for the on_press parameter.
    Returns False to stop the listener.
"""
def on_press(key):
    global c, stop_flag, started
    try: 
        if (key == keyboard.Key.space):
            if (not started):
                started = True
            else:
                if (c.is_paused and not c.is_stopped):
                    c.resume(resume_sound_file_location=fl.resume_sound_path)
                elif (not c.is_paused and not c.is_stopped):
                    c.pause(pause_sound_file_location=fl.pause_sound_path)
        elif (key == keyboard.Key.esc):
            stop_flag = True
            started = False
            if (not c.is_stopped):
                c.stop()
            #return False # Stops the keyboard listener
    except AttributeError:
        pass

def make_dirs(*paths):
    for path in paths:
        os.makedirs(path, exist_ok=True)
    return

def do_ocr():
    global c, image_path, stop_flag

    if (stop_flag):
        return
    c.resize_image(image_path)

    if (stop_flag):
        return
    # Try-Except handles the case in which no text is detected in the image
    print(image_path)
    try:
        c.ocr(image_path, fl.ocr_path)
    except TypeError:
        stop_flag = True
        # Make sure we don't get overlap with the idling sound
        while (not c.is_stopped):
            time.sleep(0.1)
        c.play(fl.no_text_sound_path)
        return
    
    if (stop_flag):
        return
    with open(fl.ocr_path, "r") as f:
        text = f.read()

    if (stop_flag):
        return
    c.make_TTS_file(text, fl.tts_path)

    return

def main():

    global c, stop_flag, started

    print("Press SPACE to start the script.")
    if(args.webcam):
        print("After starting the script, a preview of your webcam will pop up.")
        print("Press SPACE to take a picture and ESC to exit the script.")
    print("While the script is running press SPACE to pause/resume and ESC to exit.")
    print("(Note that it may take some time to terminate the program as it finishes whatever operation is was currently doing)")
    print("Waiting for input...")

    while (not started):
        if (stop_flag):
            return
        time.sleep(0.1)

    if (stop_flag):
        return
    make_dirs(os.path.basename(os.path.dirname(fl.ocr_path)), 
              os.path.basename(os.path.dirname(fl.tts_path)))
    if (args.webcam):
        make_dirs(os.path.basename(os.path.dirname(fl.image_path)))

    if (stop_flag):
        return
    global image_path
    # Define the image path based on whether the user took a picture with the
    # webcam or set a predefined location
    if (args.webcam):
        c.take_picture(fl.image_path)
        image_path = fl.image_path
    elif(args.image):
        image_path = args.image
        # Make sure the image path is actually an image that exists
        if (not os.path.isfile(image_path)):
            raise FileNotFoundError(f"Could not find image at {image_path=}")
        if (f:=os.path.splitext(image_path)[1] not in [".png", ".jpg", ".jpeg", ".bmp", ".pdf"]):
            print(f)
            raise FileNotFoundError(f"Image files must be one of: .png, .jpg, .jpeg, .bmp, .pdf.")
    print(image_path)

    if (stop_flag):
        return
    # Play an idling noise while we do ocr work
    print("\nPlease wait...\n")
    t = Thread(target=do_ocr)
    t.start()
    while (t.is_alive()):
        if (stop_flag):
            break
        c.play(fl.idling_sound_path)
        time.sleep(1)

    if (stop_flag):
        return
    c.is_stoppable = True
    c.play(fl.ready_sound_path)

    if (stop_flag):
        return
    with open(fl.ocr_path, "r") as f:
        print(f.read())

    if (stop_flag):
        return
    c.play(fl.tts_path)

    started = False
    c.is_stoppable = False

if __name__ == "__main__":

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    c = Capstone(path_to_voice=fl.voice_path)
    c.is_stoppable = False

    stop_flag = False
    started = False

    main()

    listener.stop()