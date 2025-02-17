import pygame as pg

class Sound:
    def __init__(self, gamehost):
        self.gamehost = gamehost

        pg.mixer.init()
        self.path = 'resources/sound/'

        self.space_dreams = pg.mixer.Sound(self.path + 'space dreams demo.mp3')

        self.playing_sound = False

        # demo
        # self.space_dreams.play()
        # self.space_dreams.fadeout(10)