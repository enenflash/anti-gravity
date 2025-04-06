import pygame as pg
import pygame.locals

from settings import *
from input_handler import *
from instance import *

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
            if pg.QUIT in event_types or self.input_handler.game_status() == "QUIT":
                self.running = False

            pg.display.set_caption(f"Anti-Gravity FPS: {round(self.clock.get_fps(), 2)}")
            self.delta_time = self.clock.tick(FPS)
            self.events = pg.event.get()
            self.game_state_manager.update()

class GameStateManager:
    def __init__ (self, game: Game) -> None:
        self.game = game
        self.screen = pg.display.set_mode((SCREEN_W, SCREEN_H))
        self.instance = None

        self.__launch_instance("test_map_2.json")

    def __launch_instance(self, map_name:str):
        self.instance = Instance(self.game, self.screen, map_name)
    
    def __close_instance(self):
        self.instance = None

    def end_instance(self) -> None:
        self.__close_instance()

    def update(self) -> None:
        if self.instance != None:
            self.instance.update()
            self.instance.draw()
        pg.display.flip()

if __name__ == "__main__":
    pg.init()
    new_game = Game()
    new_game.run()
    pg.quit()
    quit()