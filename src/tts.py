from piper import PiperVoice, SynthesisConfig
import wave
import time
import os
from threading import Thread
from pynput import keyboard
from audio_management import AudioManager

# Inherits from the AudioManager and FileManager classes.
class TTS(AudioManager):
    def __init__(self, path_to_voice: str, speed = float(5.0), volume = float(1.0), **kwargs):

        # Make sure that path_to_voice is a string
        if (not isinstance(path_to_voice, str)):
            raise TypeError(f"path_to_voice: {path_to_voice} must be a string")
        
        # Make sure that path_to_voice exists
        if (not os.path.isfile(path_to_voice)):
            raise OSError(f"path_to_voice: {path_to_voice} file location not found")

        # Make sure that voice rate is a float.
        if (not isinstance(speed, float)):
            raise TypeError(f"speed: {speed} must be an float")

        # Make sure that volume is a float.
        if (not isinstance(volume, float)):
            raise TypeError(f"volume: {volume} must be a float")
        
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
            self._voice.synthesize_wav(text, wav_file)

        # A while loop that sleeps for 0.1 seconds to ensure that the file gets created 
        # before exiting the function. If this isn't included, sometimes bugs can arise.
        while (not os.path.isfile(audio_file_location)):
            time.sleep(0.1)
        return