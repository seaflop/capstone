from piper import PiperVoice, SynthesisConfig
import wave
import time
import os
from threading import Thread
from pynput import keyboard
from audio_management import AudioManager

# Inherits from the AudioManager and FileManager classes.
class TTS(AudioManager):
    def __init__(self, path_to_voice: str, speed = float(1.5), volume = float(1.0), **kwargs):

        super().__init__(**kwargs)
        self._path_to_voice = path_to_voice
        self._speed= speed
        self._volume = volume

        # Initialize piper for tts and define configurations
        self._voice = PiperVoice.load(self._path_to_voice)
        self.configure_voice()

    def configure_voice(self):
        self._syn_config = SynthesisConfig(
            volume = self._volume,
            length_scale = self._speed
        )

    # Setter and getter methods for volume
    @property
    def volume(self) -> float:
        return self._volume
    
    @volume.setter
    def volume(self, volume: float):
        self._volume = volume
        self.configure_voice()
    
    # Setter and getter methods for speed
    @property
    def speed(self) -> float:
        return self._speed

    @speed.setter
    def speed(self, speed: float):
        self._speed = speed
        self.configure_voice()
        
    def make_TTS_file(self, text: str, audio_file_location: str):

        with wave.open(audio_file_location, "wb") as wav_file:
            self._voice.synthesize_wav(text, wav_file, syn_config=self._syn_config)

        # A while loop that sleeps for 0.1 seconds to ensure that the file gets created 
        # before exiting the function. If this isn't included, sometimes bugs can arise.
        while (not os.path.isfile(audio_file_location)):
            time.sleep(0.1)
        return