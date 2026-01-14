import sys
# Assert Python version >= 3.10
MIN_VERSION = (3, 10)
if sys.version_info < MIN_VERSION:
    raise EnvironmentError(f"This script requires Python version {MIN_VERSION[0]}.{MIN_VERSION[1]} or higher.\nYou are using Python version {sys.version_info.major}.{sys.version_info.minor}")

import file_locations as fl
    
from capstone import Capstone

import time
import os
from threading import Thread

def make_dirs(*paths):
    for path in paths:
        os.makedirs(path, exist_ok=True)
    return

def do_ocr():
    global c

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
    c.play(fl.ready_sound_path)

    """
    while (not started):
        if (stop_flag):
            return
        time.sleep(0.1)
    """

    if (stop_flag):
        return
    make_dirs(os.path.basename(os.path.dirname(fl.ocr_path)), 
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
    with open(fl.ocr_path, "r") as f:
        print(f.read())

    if (stop_flag):
        return
    c.play(fl.tts_path)

    c

    started = False
    

if __name__ == "__main__":

    stop_flag = False
    started = False

    c = Capstone(path_to_voice=fl.voice_path)

    main()