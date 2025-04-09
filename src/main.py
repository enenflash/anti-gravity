import pygame as pg
import pygame.locals

from settings import *
from input_handler import *
from instance import *
from menu import *

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
            self.input_handler.update()
            event_types = [i.type for i in self.events]
            if pg.QUIT in event_types:
                self.running = False
            pg.display.set_caption(f"Anti-Gravity FPS: {round(self.clock.get_fps(), 2)}")
            self.delta_time = self.clock.tick(FPS)
            self.events = pg.event.get()
            self.game_state_manager.update()

class GameStateManager:
    def __init__ (self, game: Game) -> None:
        self.game = game
        self.screen = pg.display.set_mode((screen_info.current_w, screen_info.current_h))
        self.instance = None
        self.menu = None
        
        self.launch_menu("menus/title_menu.json", "title")

    def launch_menu(self, menu_path:str, name:str):
        self.menu = Menu(self.game, name, self.screen, menu_path)

    def launch_instance(self, map_path:str):
        self.instance = Instance(self.game, self.screen, map_path)

    def close_menu(self) -> None:
        self.menu = None

    def close_instance(self) -> None:
        self.instance = None

    def game_quit(self) -> None:
        self.game.running = False

    def update(self) -> None:
        self.screen.fill("BLACK")

        if self.game.input_handler.game_status() == "PAUSE" and self.instance != None:
            self.launch_menu("menus/pause_menu.json", "pause")

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