import pytesseract
import pyttsx3
import multiprocessing
import threading
from pynput import keyboard
from pygame import mixer

# CONSTANT FOR DETERMINING IF PROGRAM IS RUNNING ON A PI
ON_PI = False

# GPIO pin designations
button = 0
potentiometer = 0

# All file locations and associated checker variables
voice_dir = "tts_output/"
current_voice_number = 1
voice_file = f"output{current_voice_number}.mp3"
max_num_of_voices = 5
image_dir = "images/"
current_image_number = 1
image_file = f"image{current_image_number}.jpg"
max_num_of_images = 5

# All pyttsx3 related variables
voice_engine = pyttsx3.init()
voices = voice_engine.getProperty('voices')
voice_type = voices[1].id
voice_rate = 140
volume = float(1.0) # MUST BE FLOAT

# All pygame mixer related variables
mixer.init()

# Set configuration for pyttsx3
voice_engine.setProperty("rate", voice_rate)
voice_engine.setProperty("volume", volume)
voice_engine.setProperty("voice", voice_type)

# Signal for handling interrupts
interrupt_signal = False    # General interrupt signal for stopping any process
pause_signal = False        # Specific signal meant for pausing/playing audio output

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
        print("key {0} was pressed".format(key.char))
    except AttributeError:
        print ("key {0} was pressed".format(key))
        if (key == keyboard.Key.space and pause_signal == False):
            pause_signal = True
        elif (key == keyboard.Key.space and pause_signal == True):
            pause_signal = False
        elif (key == key.esc):
            interrupt_signal = True
            #return False # Stops the keyboard listener

"""
    Uses pygame to play audio given the file location.
"""
def play_audio(file_location):

    global interrupt_signal, pause_signal

    is_paused = False

    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    print("listener started")

    mixer.music.load(file_location)
    mixer.music.play()
    print("playing audio")

    while (True):
        # If stop signal received and running, stop it.
        if (interrupt_signal and mixer.music.get_busy()):
            break
        # If paused signal received and running, pause it.
        elif (pause_signal and mixer.music.get_busy()):
            mixer.music.pause()
            is_paused = True
        # If unpause signal received and not running, but was paused previously, run it.
        elif (not pause_signal and not mixer.music.get_busy() and is_paused):
            mixer.music.unpause()
            is_paused = False
        # If not running and was not paused previously, stop it.
        elif (not mixer.music.get_busy() and not is_paused):
            break

    listener.stop()
    mixer.music.stop()
    reset_signals()
    print("stopping audio")

def save_TTS_to_file(text):
    voice_engine.save_to_file(text, "test.wav")
    voice_engine.runAndWait()

if __name__ == "__main__":
    text = "Take me to the island. I want to go. I want to go."
    save_TTS_to_file(text)
    play_audio("test.wav")