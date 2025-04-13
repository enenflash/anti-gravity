import pygame as pg
from src.settings import *
from src.file_loader import *

class Sound:
    """
    Responsible for sound
    """
    def __init__ (self):
        pg.mixer.init()
        sound_paths = FileLoader.open_json("sounds.json", SOUND_DATA_PATH)
        self.sounds = {}
        for sound_name in sound_paths:
            self.sounds[sound_name] = pg.mixer.Sound(sound_paths[sound_name])

        self.last_played:str = None
        self.playing_sound = False

    def play_sound(self, name:str) -> None:
        """Play a sound once """
        if VOLUME == 0 or (name not in self.sounds):
            return
        self.sounds[name].set_volume(VOLUME)
        self.sounds[name].play()

    def play_music(self, name:str) -> None:
        """Play music (only one music track can be played at a time)"""
        if VOLUME == 0 or (name not in self.sounds) or self.playing_sound:
            return
        self.sounds[name].set_volume(VOLUME)
        self.sounds[name].play(fade_ms=1000)
        self.last_played = name
        self.playing_sound = True

    def play_indefinite(self, name:str) -> None:
        """Play music indefinitely (loop)"""
        if VOLUME == 0 or (name not in self.sounds) or self.playing_sound:
            return
        self.sounds[name].set_volume(VOLUME)
        self.sounds[name].play(loops=-1, fade_ms=1000)
        self.last_played = name
        self.playing_sound = True

    def fadeout_music(self) -> None:
        """Fadeout music if currently playing anything"""
        self.playing_sound = False
        if self.last_played != None:
            self.sounds[self.last_played].fadeout(1000)

game_sound = Sound()