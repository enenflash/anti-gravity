import pygame as pg
import pygame.locals

from src.settings import *
from src.level_manager import *
from src.input_handler import *
from src.instance import *
from src.menu import *

class Game:
    """Main game class - opens a screen and handles pygame things"""
    def __init__ (self) -> None:
        self.running = True
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.events = pg.event.get()
        self.input_handler = InputHandler()
        
        self.game_state_manager = GameStateManager(self)

    def run(self) -> None:
        while self.running:
            event_types = [i.type for i in self.events]
            if pg.QUIT in event_types:
                self.running = False

            pg.display.set_caption(f"Anti-Gravity FPS: {round(self.clock.get_fps(), 2)}")
            self.delta_time = self.clock.tick(FPS)
            self.events = pg.event.get()
            self.input_handler.update(self.events)
            self.game_state_manager.update()

class GameStateManager:
    def __init__ (self, game: Game) -> None:
        self.game = game
        self.screen = pg.display.set_mode((screen_info.current_w, screen_info.current_h))
        self.instance = None
        self.menu = None

        self.level_manager = LevelManager()
        self.current_level_data = self.level_manager.get_current_level()
        self.menu_data = FileLoader.open_json("menus.json", "data/fixed/menus.json")
        
        self.launch_menu("title")
    
    def update_level(self) -> None:
        if self.instance != None:
            self.level_manager.update_level(self.instance.level_index)
    
    def launch_menu(self, name:str, bg_offset:list[int|float, int|float]=[0, 0]) -> None:
        if name not in self.menu_data:
            raise KeyError(f"{name} is not a valid menu name. check data/fixed/menus.json for valid menu names")
        self.menu = Menu(self.game, self.screen, self.menu_data[name], bg_offset)
    
    def launch_instance(self, map_path:str, level_index:int) -> None:
        self.instance = Instance(self.game, self.screen, map_path, level_index)

    def restart_instance(self) -> None:
        self.instance = Instance(self.game, self.screen, self.instance.map_path, self.instance.level_index)
    
    def close_menu(self) -> None:
        self.menu = None

    def close_instance(self) -> None:
        self.instance = None

    def set_pause_instance(self, paused:bool) -> None:
        self.instance.paused = paused

    def game_quit(self) -> None:
        self.game.running = False

    def update(self) -> None:
        self.screen.fill("BLACK")

        if self.game.input_handler.game_status() == "PAUSE" and self.instance != None and self.menu == None:
            self.set_pause_instance(True)
            self.launch_menu("pause")
        
        if self.instance != None:
            self.instance.update()
        if self.menu != None:
            self.menu.update()

        if self.instance != None:
            self.instance.draw()
        if self.menu != None:
            self.menu.draw()

        pg.display.flip()

if __name__ == "__main__":
    pg.init()
    new_game = Game()
    new_game.run()
    pg.quit()
    quit()