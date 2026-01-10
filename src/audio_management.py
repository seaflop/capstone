import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame import mixer
import time

class AudioManager():
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        mixer.init()
        mixer.set_num_channels(2)
        self._system_channel = mixer.Channel(1)
        self._is_paused = False
        self._is_stopped = True

    def __del__(self):
        mixer.quit()

    def play(self, audio_file_location: str):
        # Make sure that file_location passed was a string.
        assert isinstance(audio_file_location, str), "file_location must be a string!"

        # Make sure that file_location exists.
        assert os.path.isfile(audio_file_location), "file_location cannot be found!"

        # Make sure that file_location is a .wav file.
        assert audio_file_location.endswith(".wav"), "file_location must be a .wav file!"

        # Make sure the mixer isn't playing any other audio
        assert not mixer.music.get_busy(), "pygame mixer is already playing an audio file!"
        
        mixer.music.load(audio_file_location)
        mixer.music.play()
        self._is_paused = False
        self._is_stopped = False

        # The logic for this while loop needs to check if the mixer is busy.
        # If the mixer is not busy, we need to check if it's paused to make
        # sure that we don't exit the loop while it's paused.
        while (mixer.music.get_busy() or (not mixer.music.get_busy() and self._is_paused)):
            time.sleep(0.1)
        
        self.stop()
        
    def pause(self, pause_sound_file_location: str | None = None):
        if mixer.music.get_busy():
            mixer.music.pause()
            self._is_paused = True
        if (not pause_sound_file_location is None):
            pause_sound = mixer.Sound(pause_sound_file_location)
            self._system_channel.play(pause_sound)
            while mixer.get_busy():
                time.sleep(0.01)
            self._system_channel.stop()
        return
    
    def resume(self, resume_sound_file_location: str | None = None):
        if not mixer.music.get_busy():
            if (not resume_sound_file_location is None):
                resume_sound = mixer.Sound(resume_sound_file_location)
                self._system_channel.play(resume_sound)
                while mixer.get_busy():
                    time.sleep(0.01)
                self._system_channel.stop()
            mixer.music.unpause()
            self._is_paused = False
        return
    
    def stop(self, stop_sound_file_location: str | None = None):
        mixer.music.stop()
        mixer.music.unload()
        self._is_paused = False
        self._is_stopped = True
        if (not stop_sound_file_location is None):
            stop_sound = mixer.Sound(stop_sound_file_location)
            self._system_channel.play(stop_sound)
            while (mixer.get_busy()):
                time.sleep(0.01)
            self._system_channel.stop()
        return

    # Getter and setter methods for is_paused
    @property
    def is_paused(self) -> bool:
        return self._is_paused
    
    @is_paused.setter
    def is_paused(self, is_paused: bool):
        self._is_paused = is_paused

    # Getter and setter methods for is_stopped
    @property
    def is_stopped(self) -> bool:
        return self._is_stopped
    
    @is_stopped.setter
    def is_stopped(self, is_stopped: bool):
        self._is_stopped = is_stopped