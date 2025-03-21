import pygame as pg
from settings import *
from map import *
from player import *

class Instance:
    def __init__ (self, game:object, screen:pg.Surface, map_name:str) -> None:
        self.game = game
        self.screen = screen
        self.surface = pg.Surface((SCREEN_W, SCREEN_H), pg.SRCALPHA)

        self.map_name = map_name
        self.map = Map(self, map_name)
        self.player = Player(self, self.map.player_start_x, self.map.player_start_y)
        self.map.set_up_camera()

    def update(self) -> None:
        self.player.update()
        self.map.update()
    
    def draw(self) -> None:
        self.surface.fill("BLACK")
        self.map.draw() # player is drawn inside map draw function
        self.screen.blit(self.surface, (0, 0))