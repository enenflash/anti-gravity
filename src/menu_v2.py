import json, pygame as pg
from settings import *
from background import *
from menu_elements import *
from mouse_control import *

class Screen:
    def __init__(self, menu, elements:list=[], poppable=False, background_fade=0):
        self.menu = menu
        self.elements = elements
        self.poppable = poppable

        self.background_rect = pg.Rect(0, 0, SCREEN_W, SCREEN_H)
        self.background_fade = background_fade

    def update(self):
        for i in self.elements:
            i.update()

    def draw(self):
        if self.background_fade != 0:
            pg.draw.rect(self.menu.screen, (0, 0, 0, self.background_fade), self.background_rect)
        for i in self.elements:
            i.draw()

class ImageHandler:
    def __init__(self, menu):
        self.menu = menu

        self.btn_border = self.get_texture(self.menu.image_paths["btn_border"], TILE_SIZE*9, "h")
        self.active_btn_border = self.get_texture(self.menu.image_paths["active_btn_border"], TILE_SIZE*9, "h")

    def get_texture(self, path, scale, m):
        image = pg.image.load(path).convert_alpha()
        return self.image_scale(image, scale, m)
    
    def image_scale(self, image, scale, m):
        if m == "w": scale = scale / image.get_width()
        else: scale = scale / image.get_height()
        return pg.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))

class MenuScreen:
    def __init__(self, gamehost):
        self.gamehost = gamehost
        self.screen = pg.Surface((SCREEN_W, SCREEN_H), pg.SRCALPHA)
        self.background = Background(self.gamehost, self.screen)
        self.bg_offset = [0, 0]

        self.mouse = Mouse(self)

        self.draw_background = True
        self.layers = []

        with open("json/menu_resources.json", "r") as file:
            self.image_paths = json.load(file)

        self.image_handler = ImageHandler(self)

        self.title_screen = Screen(self, [
            TextBox(self, self.image_paths["title"], screen_info.current_w/1.5, (HALF_SCREEN_W, HALF_SCREEN_H-TILE_SIZE*5)), 
            ButtonDiv(self, ["PLAY", "SETTINGS", "QUIT"], [
                self.image_paths["play_btn"],
                self.image_paths["settings_btn"],
                self.image_paths["quit_btn"]
            ], TILE_SIZE*7, (HALF_SCREEN_W, HALF_SCREEN_H+50))
        ])

        self.pause_screen = Screen(self, [
            TextBox(self, self.image_paths["paused"], screen_info.current_w/1.5, (HALF_SCREEN_W, HALF_SCREEN_H-TILE_SIZE*5)),
            ButtonDiv(self, ["RESUME", "MAIN_MENU", "QUIT"], [
                self.image_paths["resume_btn"],
                self.image_paths["main_menu_btn"],
                self.image_paths["quit_btn"]
            ], TILE_SIZE*7, (HALF_SCREEN_W, HALF_SCREEN_H+50))
        ], poppable=True, background_fade=150)

        self.load_layer(self.title_screen)
        self.button_selected = ""

    def button_pressed(self, button_selected):
        if self.button_selected == "PLAY":
            self.gamehost.game_state = "GAME"
            self.clear_layers()
            self.gamehost.launch_game("test_maps(v3).json", "test_map")
            self.gamehost.sound.space_dreams.fadeout(1000)

        elif self.button_selected == "QUIT":
            self.gamehost.game_state = "QUIT"

        elif self.button_selected == "RESUME":
            self.resume_game()

        elif self.button_selected == "MAIN_MENU":

            self.clear_layers()
            self.gamehost.close_game()

            self.load_layer(self.title_screen)
            self.draw_background = True
            self.gamehost.sound.space_dreams.play()
    
    def update(self):
        self.mouse.update()

        if self.draw_background:
            self.bg_offset[0] -= 0.6
            self.bg_offset[0] %= BG_SIZE
            self.bg_offset[1] -= 0.3
            self.bg_offset[1] %= BG_SIZE

        for layer in self.layers:
            layer.update()

        if pg.K_SPACE in self.gamehost.keydowns or pg.K_RETURN in self.gamehost.keydowns:
            self.button_pressed(self.button_selected)

    def clear_layers(self):
        self.layers = []
        self.draw_background = False

    def load_layer(self, screen):
        self.layers.append(screen)

    @property
    def num_layers(self):
        return len(self.layers)

    @property
    def num_poppable(self):
        unpoppable = [layer for layer in self.layers if layer.poppable]
        return len(unpoppable)

    def remove_layer(self, index):
        if index in range(0, len(self.layers)):
            self.layers.pop(index)

    def pop_layer(self):
        if len(self.layers) != 0:
            if self.layers[-1] == self.pause_screen:
                self.resume_game()
                return None
            self.layers.pop()

    def pause_game(self):
        self.clear_layers()
        self.load_layer(self.pause_screen)
        self.gamehost.pause_game()
        #self.draw_background = True

    def resume_game(self):
        self.clear_layers()
        self.gamehost.continue_game()
        self.gamehost.game_state = "GAME"
        
    def draw(self):
        self.screen.fill("BLACK")

        if self.draw_background:
            self.background.draw_static(self.bg_offset)
        
        for layer in self.layers:
            layer.draw()

        self.mouse.draw()

        if len(self.layers) > 0:
            self.gamehost.screen.blit(self.screen, (0, 0))