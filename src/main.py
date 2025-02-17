import pygame as pg

from settings import *
from sound import *
from menu_v2 import *
from background import *
from player import *
from map import *
from debug import *

class Game:
    def __init__(self, gamehost, screen, map_json, map_name):
        self.gamehost = gamehost

        self.delta_time = 1
        self.paused = False

        self.screen = screen
        self.surface = pg.Surface((SCREEN_W, SCREEN_H), pg.SRCALPHA)

        self.keys = gamehost.keys
        self.keydowns = []

        self.events = pg.event.get()

        self.background = Background(self, self.surface)
        self.player = Player(self)
        self.map = Map(self, map_json, map_name)

    def update(self):
        if self.paused:
            return None
        
        self.delta_time = self.gamehost.delta_time

        self.keys = self.gamehost.keys
        self.keydowns = self.gamehost.keydowns

        self.events = self.gamehost.events

        self.player.update()
        self.map.update()

    def draw(self):
        self.surface.fill("BLACK")

        self.background.draw()
        self.player.draw()
        self.map.draw()

        self.screen.blit(self.surface, (0, 0))

class GameHost:
    def __init__(self):
        print("[*] Launching ANTI-GRAVITY . . .")
        self.running = True
        self.game_state = "MENU"

        self.screen = pg.display.set_mode((SCREEN_W, SCREEN_H))
        
        self.clock = pg.time.Clock()
        self.delta_time = 1

        self.keys = pg.key.get_pressed()
        self.keydowns = []

        self.events = pg.event.get()

        self.menu_screen = MenuScreen(self)
        self.game = None

        self.sound = Sound(self)
        if VOLUME != 0:
            self.sound.space_dreams.play()

        self.debug_console = DebugConsole(self)

        print("[#] ANTI-GRAIVTY Launched")

    def launch_game(self, map_json, map_name):
        self.game = Game(self, self.screen, map_json, map_name)
        print(f"[*] Opening {map_name} from {map_json.split('.')[0]} . . .")

    def pause_game(self):
        if self.game != None:
            self.game.paused = True

    def continue_game(self):
        if self.game != None:
            self.game.paused = False

    def close_game(self):
        self.game = None
        print("[#] Closed current game")

    def update_game(self):
        if self.game != None:
            self.game.update()

    def draw_game(self):
        if self.game != None:
            self.game.draw()

    def clear_menu(self):
        self.menu_screen.clear_layers()

    def find_keydowns(self):
        keydown_events = [event for event in self.events if event.type == pg.KEYDOWN]
        self.keydowns = [event.key for event in keydown_events]

    def update(self):
        pg.display.set_caption(f"Anti-Gravity FPS: {round(self.clock.get_fps(), 2)}")
        self.delta_time = self.clock.tick(FPS)

        self.keys = pg.key.get_pressed()
        self.find_keydowns()

        self.events = pg.event.get()

        #if self.game_state == "MENU":
        self.menu_screen.update()
        #elif self.game_state == "GAME":
        self.update_game()

        if pg.K_q in self.keydowns:
            self.debug_console.input_command()
        
        if pg.K_ESCAPE in self.keydowns:
            #if self.game_state == "GAME":
            #    self.game_state = "MENU"
            #    self.menu_screen.pause_game()
            #elif self.game_state == "MENU":
            #    self.game_state = "QUIT"
            if self.menu_screen.num_poppable > 0:
                self.menu_screen.pop_layer()
            elif self.menu_screen.num_layers == 0:
                self.menu_screen.pause_game()

    def draw(self):
        self.screen.fill("BLACK")

        #if self.game_state == "GAME":
        self.draw_game()
        #elif self.game_state == "MENU":
        self.menu_screen.draw()

        pg.display.flip()

    def run(self):
        while self.running:

            event_types = [i.type for i in self.events]
            if pg.QUIT in event_types or self.game_state == "QUIT":
                print("[*] ANTI-GRAVITY closing . . .")
                self.running = False

            self.update()
            self.draw()

if __name__ == "__main__":
    pg.init()
    new_game = GameHost()
    new_game.run()
    pg.quit()
    quit()