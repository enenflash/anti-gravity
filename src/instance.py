import pygame as pg, time
from src.settings import *
from src.map import *
from models.entities import *
from src.background import *
from src.sound import *

# not the best class name but it would be a pain to change the name across 2000 lines of code :)
class Instance:
    """
    Represents a game currently being played.
    \nCall update() every loop and draw() to draw the game
    """
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

        self.blend_image_ver = pg.Surface((TILE_SIZE*3+(self.screen.get_width()-SCREEN_W)/2, SCREEN_H), pg.SRCALPHA)
        self.blend_image_hor = pg.Surface((self.screen.get_width(), TILE_SIZE*2), pg.SRCALPHA)
        self.blend_image_ver.fill([0, 0, 0, 100])
        self.blend_image_hor.fill([0, 0, 0, 150])

        game_sound.play_indefinite("ambience")

        self.start_time = time.time()

    def update(self) -> None:
        if self.paused:
            return
        
        self.player.update()
        self.map.update()

        if self.map.check_win():
            game_sound.play_sound("victory")
            time_taken = round(time.time()-self.start_time, 2)
            self.game.game_state_manager.set_pause_instance(True)
            self.game.game_state_manager.launch_menu("win", menu_vars={"time":time_taken, "level_index": self.level_index})
            self.game.game_state_manager.update_level(self.level_index)
            self.game.game_state_manager.update_high_score(self.level_index, time_taken)

        if self.map.check_die():
            game_sound.play_sound("lazer")
            game_sound.play_sound("game-over")
            game_sound.fadeout_music()
            game_sound.play_indefinite("moonlight-sonata")
            self.game.game_state_manager.set_pause_instance(True)
            self.game.game_state_manager.launch_menu("sorry", menu_vars={"time":round(time.time()-self.start_time, 2), "level_index": self.level_index})
            self.game.game_state_manager.update_level(self.level_index)
    
    def draw(self) -> None:
        self.surface.fill([0, 0, 0, 0])
        self.background.draw(self.map.camera.x, self.map.camera.y)
        self.map.draw() # player is drawn inside map draw function
        self.screen.blit(self.surface, ((self.screen.get_width()-SCREEN_W)/2, 0))
        self.screen.blit(self.blend_image_ver, (0, 0))
        self.screen.blit(self.blend_image_ver, (self.screen.get_width()-self.blend_image_ver.get_width(), 0))
        self.screen.blit(self.blend_image_hor, (0, 0))
        self.screen.blit(self.blend_image_hor, (0, self.screen.get_height()-self.blend_image_hor.get_height()))