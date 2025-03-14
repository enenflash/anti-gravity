import pygame as pg
from settings import *

class Instance:
    def __init__ (self, game:object, screen:pg.Surface, map_name:str) -> None:
        self.game = game
        self.screen = screen
        self.surface = pg.Surface((SCREEN_W, SCREEN_H), pg.SRCALPHA)

        self.map_name = map_name

    def update(self) -> None:
        pass
    
    def draw(self) -> None:
        self.surface.fill("BLACK")
        self.screen.blit(self.surface, (0, 0))