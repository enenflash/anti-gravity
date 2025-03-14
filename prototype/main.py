import pygame as pg

from settings import *
from sound import *
from input_handler import *
from player import *
from map import *

# #23001E

class Game:
    def __init__ (self) -> None:
        print("[*] Launching ANTI-GRAVITY . . .")
        self.running = True
        self.instance = None

        self.screen = pg.display.set_mode((SCREEN_W, SCREEN_H))
        
        self.clock = pg.time.Clock()
        self.delta_time = 1

        self.events = pg.event.get()

        self.sound = Sound()
        self.input_handler = InputHandler()

        print("[#] ANTI-GRAIVTY Launched")

    def __launch_instance(self, map_name:str):
        self.instance = Instance(self, map_name)

    def __close_instance(self):
        self.instance = None

    def end_instance(self) -> None:
        self.__close_instance()

    def update(self):
        pg.display.set_caption(f"Anti-Gravity FPS: {round(self.clock.get_fps(), 2)}")
        self.delta_time = self.clock.tick(FPS)
        
        self.events = pg.event.get()

        # check keydowns
        self.input_handler.update()

        # update instance
        if self.instance != None:
            self.instance.update()

    def draw(self):
        self.screen.fill("BLACK")

        # draw instance
        if self.instance != None:
            self.instance.draw()

        pg.display.flip()

    def run(self):
        self.__launch_instance("new_map.json")
        while self.running:
            event_types = [i.type for i in self.events]
            if pg.QUIT in event_types or self.input_handler.game_status() == "QUIT":
                print("[*] ANTI-GRAVITY closing . . .")
                self.running = False

            self.update()
            self.draw()

class Instance:
    def __init__ (self, game:Game, map_name:str) -> None:
        self.game = game
        self.surface = pg.Surface((SCREEN_W, SCREEN_H), pg.SRCALPHA)

        self.delta_time = 1
        self.paused = False

        self.map_name = map_name
        self.map = Map(self, map_name)
        self.player = Player(self)

        self.map.set_up_camera()

    def end_instance(self) -> None:
        self.game.end_instance()

    def reset_map(self) -> None:
        self.map = Map(self, self.map_name)
        self.player = Player(self)

        self.map.set_up_camera()
    
    def update(self) -> None:
        self.player.update()
        self.map.update()

        if self.game.input_handler.game_status() == "RESTART":
            self.reset_map()
    
    def draw(self) -> None:
        self.surface.fill("BLACK")

        self.map.draw()

        self.game.screen.blit(self.surface, (0, 0))

if __name__ == "__main__":
    pg.init()
    new_game = Game()
    new_game.run()
    pg.quit()
    quit()