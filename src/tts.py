import pyttsx3
from pynput import keyboard
from pygame import mixer
import logging
logging.basicConfig(level=logging.INFO, format = " %(asctime)s - %(levelname)s - %(message)s")
#logging.disable(logging.CRITICAL) # COMMENT OUT THIS LINE TO DISABLE LOGGING MESSAGES
import os
import time

import file_management as fm

# Initialize and configure pyttsx3
voice_engine = pyttsx3.init()
voices = voice_engine.getProperty('voices')
voice_type = voices[1].id
voice_rate = 120
volume = float(1.0) # MUST BE FLOAT
voice_engine.setProperty("rate", voice_rate)
voice_engine.setProperty("volume", volume)
voice_engine.setProperty("voice", voice_type)

# Initialize pygame mixer for audio output
mixer.init()

# Signal for handling audio interrupts
interrupt_signal = False    # General interrupt signal for stopping any process
pause_signal = False        # Specific signal meant for pausing/playing audio output

"""
    This function checks for key presses.
    It is used as part of the keyboard.Listener() for the on_press parameter.
    Returns False to stop the listener.
"""
def on_press(key):
    global interrupt_signal, pause_signal
    try: 
        logging.info("key {0} was pressed".format(key.char))
    except AttributeError:
        logging.info("key {0} was pressed".format(key))
        if (key == keyboard.Key.space and pause_signal == False):
            pause_signal = True
            logging.info(f"Pause signal set to {pause_signal}")
        elif (key == keyboard.Key.space and pause_signal == True):
            pause_signal = False
            logging.info(f"Pause signal set to {pause_signal}")
        elif (key == key.esc):
            interrupt_signal = True
            logging.info(f"Interrupt signal set to {interrupt_signal}")
            #return False # Stops the keyboard listener

def reset_signals():
    global interrupt_signal, pause_signal
    interrupt_signal = False
    pause_signal = False

"""
    Uses pygame to play audio given the file location.
"""
def play_audio(file_location: str):
    
    # Make sure that the function call passed a string as the file_location parameter
    assert isinstance(file_location, str), "File location passed must be a string."

    # Make sure that the passed file_location parameter is a valid file location
    assert os.path.isfile(file_location), "Error finding audio file"

    global interrupt_signal, pause_signal

    is_paused = False

    # Start listening for keyboard events
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    logging.info("Started keyboard listener")

    # Start playing audio
    mixer.music.load(file_location)
    mixer.music.play()
    logging.info("Playing audio")

    while (True):
        # If stop signal received and running, stop it.
        if (interrupt_signal and mixer.music.get_busy()):
            break
        # If stop signal received and paused, stop it.
        elif (interrupt_signal and is_paused):
            break
        # If paused signal received and running, pause it.
        elif (pause_signal and mixer.music.get_busy()):
            mixer.music.pause()
            is_paused = True
            logging.info("Paused audio")
        # If unpause signal received and not running, but was paused previously, run it.
        elif (not pause_signal and not mixer.music.get_busy() and is_paused):
            mixer.music.unpause()
            is_paused = False
            logging.info("Resumed audio")
        # If not running and was not paused previously, stop it.
        elif (not mixer.music.get_busy() and not is_paused):
            break

    logging.info("Stopping keyboard listener")
    listener.stop()
    logging.info("Stopping audio playback")
    mixer.music.stop()
    logging.info("Resetting all signals")
    reset_signals()

def TTS_to_file(text: str):

    # Make sure that the function call passed a string as the text parameter
    assert isinstance(text, str), "Text passed must be a string."

    logging.info("Checking to make sure the file does not already exist")
    fm.shift_files(fm.base_tts_file, directory=fm.tts_dir, max_num_of_files=5)

    """
    logging.info("Checking to make sure the file does not already exist")
    if (os.path.isfile(tts_path)):
        os.remove(tts_path)
        logging.info("Removed already existing audio file")
    """

    logging.info("Text received")
    voice_engine.save_to_file(text, fm.tts_path)
    voice_engine.runAndWait()

    # A while loop that sleeps for 0.1 seconds to ensure that the file gets created 
    # before exiting the function.
    while (not os.path.isfile(fm.tts_path)):
        time.sleep(0.1)
        logging.info("Slept for 0.1 seconds while waiting for .wav file creation")

    logging.info(f"TTS saved to {fm.tts_path}")