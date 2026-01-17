import sys
# Assert Python version >= 3.10
MIN_VERSION = (3, 10)
if sys.version_info < MIN_VERSION:
    raise EnvironmentError(f"This script requires Python version {MIN_VERSION[0]}.{MIN_VERSION[1]} or higher.\nYou are using Python version {sys.version_info.major}.{sys.version_info.minor}")

import file_locations as fl
    
from capstone_rpi import Capstone

import time
import os
from threading import Thread
from gpiozero import Button

BUTTON_PIN = 17

def handle_press():
    global c, stop_flag, started
    # If the button is pressed:
    # 1. Start the script if it has not yet been started
    # 2. Pause/Play audio output if audio is playing
    if (not started):
        started = True
    else:
        if (c.is_paused and not c.is_stopped):
            c.resume(resume_sound_file_location=fl.resume_sound_path)
        elif (not c.is_paused and not c.is_stopped):
            c.pause(pause_sound_file_location=fl.pause_sound_path)
    return

def handle_hold():
    global c, stop_flag, started
    # Holding the button for 3 seconds will either:
    # 1. Exit the current iteration of the image->tts pipeline if the iteration is running
    # 2. Exit the program entirely if we're not doing any work
    if (started):
        stop_flag = True
        started = False
        if (not c.is_stopped):
            c.stop()
    # Remove this later: We're going to replace this function with a switch
    else:
        sys.exit()

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

    print("Press the button to start the script.")
    print("While the script is running press the button to pause/resume and hold the button to exit.")
    print("(Note that it may take some time to terminate the program as it finishes whatever operation is was currently doing)")
    print("Waiting for input...")

    while (not started):
        if (stop_flag):
            return
        time.sleep(0.1)

    if (stop_flag):
        return
    make_dirs(os.path.basename(os.path.dirname(fl.ocr_path)), 
              os.path.basename(os.path.dirname(fl.tts_path)),
              os.path.basename(os.path.dirname(fl.image_path)))

    if (stop_flag):
        return
    global image_path
    image_path = fl.image_path

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

    return

if __name__ == "__main__":

    c = Capstone(path_to_voice=fl.voice_path)

    button = Button(pin = BUTTON_PIN, bounce_time = 0.1, hold_time = 3.0)
    button.when_pressed(handle_press)
    button.when_held(handle_hold)

    while (True):
        # We want to reset these flags every time we exit out of the main loop
        c.is_stoppable = False
        stop_flag = False
        started = False
        main()