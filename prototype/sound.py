import pygame as pg
from settings import *

class Sound:
    def __init__ (self):
        pg.mixer.init()
        self.path = 'resources/sound/'
        
        self.sounds = {
            "quack": pg.mixer.Sound(self.path + 'quack.mp3'),
            "victory": pg.mixer.Sound(self.path + 'victory.mp3')
        }

    def play_sound(self, name:str) -> None:
        if VOLUME == 0:
            return
        if name not in self.sounds:
            print(f"{name} not in sound library")
            return
        self.sounds[name].play()