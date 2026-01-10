import sys
# Assert Python version >= 3.10
MIN_VERSION = (3, 10)
if sys.version_info < MIN_VERSION:
    raise EnvironmentError(f"This script requires Python version {MIN_VERSION[0]}.{MIN_VERSION[1]} or higher.\nYou are using Python version {sys.version_info.major}.{sys.version_info.minor}")

import file_locations as fl
# Ensure the proper starting directory (i.e. not from src/ and instead from the project root directory)
if (sys.argv[0] != fl.realmain_script_path):
    raise RuntimeError(f"Script must be run from {fl.main_script_path}. Got {sys.argv[0]}")
    
from capstone import Capstone

import time
import os
from threading import Thread
from gpiozero import Button
from picamera2 import Picamera2

camera = Picamera2()
camera_config = camera.create_still_configuration(main={"size": (1920, 1080)})
camera.configure(camera_config)
camera.start()

BUTTON_PIN = 14
BUTTON_HOLD_TIME = 3

def button_hold_handler():
    global stop_flag
    if (started):
        stop_flag = True

def button_press_handler():
    global c, started
    if (not started):
        started = True
        main()
    else:
        if (c.is_paused and not c.is_stopped):
            c.resume(resume_sound_file_location=fl.resume_sound_path)
        elif (not c.is_paused and not c.is_stopped):
            c.pause(pause_sound_file_location=fl.pause_sound_path)
    return

def take_picture():
    global camera
    camera.capture_file(fl.image_path)
    return

def do_ocr():
    global c, stop_flag

    if (stop_flag):
        return
    take_picture()

    if (stop_flag):
        return
    c.resize_image(fl.image_path)

    if (stop_flag):
        return
    c.ocr(fl.image_path, fl.ocr_path)
    
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

    if (stop_flag):
        return
    c.create_path(os.path.basename(os.path.dirname(fl.ocr_path)), 
                  os.path.basename(os.path.dirname(fl.tts_path)),
                  os.path.basename(os.path.dirname(fl.image_path)))

    if (stop_flag):
        return
    t = Thread(target=do_ocr)
    t.start()
    while (t.is_alive()):
        c.play(fl.idling_sound_path)
        time.sleep(1)
    
    if (stop_flag):
        return
    c.play(fl.tts_path)

if __name__ == "__main__":

    program_running = True

    stop_flag = False
    started = False

    c = Capstone(path_to_voice=fl.voice_path)
    c.play(fl.ready_sound_path)

    print("Press the button to start the script.")
    print("While the script is running press the button to pause/resume and hold down the button to exit.")
    print("(Note that it may take some time to terminate the program as it finishes whatever operation is was currently doing)")
    print("Waiting for input...")

    main()

    stop_flag = False
    started = False