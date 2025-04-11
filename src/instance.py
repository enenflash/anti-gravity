import pygame as pg
from settings import *
from map import *
from player import *
from background import *

class Instance:
    def __init__ (self, game:object, screen:pg.Surface, map_path:str) -> None:
        self.game = game
        self.screen = screen
        self.surface = pg.Surface((SCREEN_W, SCREEN_H), pg.SRCALPHA)
        self.paused = False

        self.map_path = map_path
        self.map = Map(self, map_path)
        self.player = Player(self, self.map.player_start_x, self.map.player_start_y)
        self.map.set_up()
        self.background = DynamicBackground(self.screen, "resources/background.png")

    def update(self) -> None:
        if self.paused:
            return
        
        self.player.update()
        self.map.update()
    
    def draw(self) -> None:
        self.surface.fill([0, 0, 0, 0])
        self.background.draw(self.map.camera.x, self.map.camera.y)
        self.map.draw() # player is drawn inside map draw function
        self.screen.blit(self.surface, ((screen_info.current_w-SCREEN_W)/2, 0))