import pygame as pg
from src.settings import *
from src.map import *
from models.entities import *
from src.background import *
from src.sound import *

class Instance:
    def __init__ (self, game:object, screen:pg.Surface, map_path:str, level_index:int) -> None:
        self.game = game
        self.screen = screen
        self.surface = pg.Surface((SCREEN_W, SCREEN_H), pg.SRCALPHA)
        self.paused = False
        self.level_index = level_index

        self.map_path = map_path
        self.map = Map(self, map_path)
        self.player = Player(self, self.map.player_start_x, self.map.player_start_y)
        self.map.set_up()
        self.background = DynamicBackground(self.screen, "resources/background.png")

        self.blend_image = pg.Surface((TILE_SIZE*3+(self.screen.get_width()-SCREEN_W)/2, SCREEN_H), pg.SRCALPHA)
        
        game_sound.play_indefinite("ambience")

    def update(self) -> None:
        if self.paused:
            return
        
        self.player.update()
        self.map.update()

        if self.map.check_win():
            game_sound.play_sound("victory")
            self.game.game_state_manager.set_pause_instance(True)
            self.game.game_state_manager.launch_menu("win")
            self.game.game_state_manager.update_level()

        if self.map.check_die():
            self.game.game_state_manager.set_pause_instance(True)
            self.game.game_state_manager.launch_menu("sorry")
            self.game.game_state_manager.update_level()
    
    def draw(self) -> None:
        self.surface.fill([0, 0, 0, 0])
        self.background.draw(self.map.camera.x, self.map.camera.y)
        self.map.draw() # player is drawn inside map draw function
        self.screen.blit(self.surface, ((self.screen.get_width()-SCREEN_W)/2, 0))
        self.blend_image.fill([0, 0, 0, 100])
        self.screen.blit(self.blend_image, (0, 0))
        self.screen.blit(self.blend_image, (self.screen.get_width()-self.blend_image.get_width(), 0))