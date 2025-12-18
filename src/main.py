import pytesseract
import pyttsx3
import multiprocessing
import threading
from pynput import keyboard
from pygame import mixer
import os
import sys
import time
import logging
logging.basicConfig(level=logging.INFO, format = " %(asctime)s - %(levelname)s - %(message)s")
#logging.disable(logging.CRITICAL) # COMMENT OUT THIS LINE TO DISABLE LOGGING MESSAGES

# CONSTANT FOR DETERMINING IF PROGRAM IS RUNNING ON A RASPBERRY PI
ON_PI = False

# GPIO pin designations
button = 0
potentiometer = 0

# All file locations
tts_dir = "./tts_output"
tts_file = "tts1.wav"
tts_path = os.path.join(tts_dir, tts_file)
base_tts_file = "tts.wav"

image_dir = "./images"
image_file = "image1.jpg"
image_path = os.path.join(image_dir, image_file)
base_image_file = "image.jpg"

# Initialize and configure pyttsx3
voice_engine = pyttsx3.init()
voices = voice_engine.getProperty('voices')
voice_type = voices[1].id
voice_rate = 140
volume = float(1.0) # MUST BE FLOAT
voice_engine.setProperty("rate", voice_rate)
voice_engine.setProperty("volume", volume)
voice_engine.setProperty("voice", voice_type)

# Initialize pygame mixer for audio output
mixer.init()

# Signal for handling interrupts
interrupt_signal = False    # General interrupt signal for stopping any process
pause_signal = False        # Specific signal meant for pausing/playing audio output

"""
    This function recursively shifts files and renames them to open space
    for a new file.
    Takes a parameter for the directory we wish to perform the shift in,
    the base name of the file that we wish to perform actions on, and the
    maximum number of those files we want to keep.
    e.g. 
        directory = ./testing
        base_name = test.txt
        max_num_of_files = 4

        ./testing/test5.txt -> deleted
        ./testing/test4.txt -> deleted
        ./testing/test3.txt -> test4.txt
        ./testing/hello.wav -> unaffected
        ./testing/test2.txt -> test3.txt
        ./testing/test.py   -> unaffected
        ./testing/test.txt  -> unaffected
        ./testing/test1.txt -> test2.txt

        This allows us to create a new test1.txt elsewhere in the program 
        and not overwrite any old files.
    
    By default checks in the project folder directory and only allows for
    one file of the base_name type.
"""
def shift_files(base_name: str, directory = ".", max_num_of_files = 1):

    # Make sure that the passed directory is a string and exists.
    assert isinstance(directory, str), "directory must be passed as a string"
    assert os.path.exists(directory), "Error finding directory"
    
    # Make sure that the passed base_name is a string and that a "." exists
    # somewhere in the file name.
    assert isinstance(directory, str), "directory must be passed as a string"
    assert "." in base_name, "base_name must contain a . somewhere in the string"

    # Make sure that max_num_of_files is an integer

    assert isinstance(max_num_of_files, int), "max_num_of_files must be an integer"
    # Split the string at the last "." to split the name and file extension.
    # Returns a tuple containing the prefix, delimiter, and postfix.
    # of the string.
    parts = base_name.partition(".") 
    logging.info(f"Rarts of the base name are {parts}")

    # Make sure that at least one file of the type base_name exists in the directory
    # passed. Return if not found.
    test_file = f"{parts[0]}1{parts[1]}{parts[2]}"
    test_file_path = os.path.join(directory, test_file)
    logging.info(f"Looking for {test_file_path}")
    if not (os.path.isfile(test_file_path)):
        logging.warning(f"Could not find {test_file_path}")
        return
    else:
        logging.info(f"Found {test_file_path}")

    # Define a path for the largest possible numbered file
    count_up = 0
    file = f"{parts[0]}{max_num_of_files + count_up}{parts[1]}{parts[2]}"
    file_path = os.path.join(directory, file)
    logging.info(f"Defined path for {file_path}")
    
    # Delete extra files
    while(os.path.isfile(file_path)):
        os.remove(file_path)
        logging.info(f"Removed {file_path}")
        count_up += 1
        file = f"{parts[0]}{max_num_of_files + count_up}{parts[1]}{parts[2]}"
        file_path = os.path.join(directory, file)

    file_new = f"{parts[0]}{max_num_of_files}{parts[1]}{parts[2]}"
    file_new_path = os.path.join(directory, file_new)
    # Shift remaining files
    for i in range(max_num_of_files, 1, -1):
        logging.info(i)
        file_current = f"{parts[0]}{i - 1}{parts[1]}{parts[2]}"
        file_current_path = os.path.join(directory, file_current)
        if(os.path.isfile(file_current_path)):
            os.rename(file_current_path, file_new_path)
        file_new = file_current
        file_new_path = os.path.join(directory, file_new)
    
    """
    # Recursively call the function to shift all files
    if (max_num_of_files == 1):
        return
    else:
        max_num_of_files -= 1
        shift_files(directory, base_name, max_num_of_files)
    """
    

def reset_signals():
    global interrupt_signal, pause_signal
    interrupt_signal = False
    pause_signal = False

def get_voice_file_location():
    global voice_dir, voice_file
    return voice_dir + voice_file

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

    global tts_path
    
    # Make sure that the function call passed a string as the text parameter
    assert isinstance(text, str), "Text passed must be a string."

    logging.info("Checking to make sure the file does not already exist")
    if (os.path.isfile(tts_path)):
        os.remove(tts_path)
        logging.info("Removed already existing audio file")

    logging.info("Text received")
    voice_engine.save_to_file(text, tts_path)
    voice_engine.runAndWait()

    # A while loop that sleeps for 0.1 seconds to ensure that the file gets created 
    # before exiting the function.
    while (not os.path.isfile(tts_path)):
        time.sleep(0.1)
        logging.info("Slept for 0.1 seconds while waiting for .wav file creation")

    logging.info("TTS saved")

if __name__ == "__main__":
    logging.info("Beginning of program")
    text = "I want to go to the island. Why won't you let me go? Let me go."
    TTS_to_file(text)
    play_audio(tts_path)
    shift_files("tts.wav", directory=tts_dir, max_num_of_files=3)