import pygame as pg, json
from settings import *

class Mouse:
    def __init__(self, menu):
        self.menu = menu
        pg.mouse.set_visible(False)

        with open("json/menu_resources.json", "r") as file:
            self.mouse_images = json.load(file)["mouse"]

        self.mouse_image = pg.image.load(self.mouse_images["idle"]).convert_alpha()
        self.mouse_image = pg.transform.scale(self.mouse_image, (TILE_SIZE, TILE_SIZE))

        self.click_animation = self.get_image(self.mouse_images["click"])

        mouse_button_events = [event for event in self.menu.gamehost.events if event.type == pg.MOUSEBUTTONDOWN]
        self.buttons_down = [event.mouse for event in mouse_button_events]
        mouse_button_events = [event for event in self.menu.gamehost.events if event.type == pg.MOUSEBUTTONUP]
        self.buttons_up = [event.mouse for event in mouse_button_events]

        self.pos = pg.mouse.get_pos()

        self.animation_index = -1

    def get_image(self, sprite_sheet_path):
        sprite_sheet_image = pg.image.load(sprite_sheet_path).convert_alpha()
        length = sprite_sheet_image.get_rect()[2]

        images = []
        for i in range(length//16):
            image = sprite_sheet_image.subsurface((i*16, 0, 16, 16))
            images.append(pg.transform.scale(image, (TILE_SIZE, TILE_SIZE)))

        return images
    
    @property
    def pressed(self):
        return 1 in self.buttons_up
    
    def animate_click(self):
        self.animation_index += 1
        if self.animation_index == len(self.click_animation):
            self.animation_index = -1

    def update(self):
        mouse_button_events = [event for event in self.menu.gamehost.events if event.type == pg.MOUSEBUTTONDOWN]
        self.buttons_down = [event.button for event in mouse_button_events]
        mouse_button_events = [event for event in self.menu.gamehost.events if event.type == pg.MOUSEBUTTONUP]
        self.buttons_up = [event.button for event in mouse_button_events]

        self.pos = pg.mouse.get_pos()

        if self.animation_index != -1:
            self.animate_click()

        if self.pressed:
            self.animation_index = 0

    def draw(self):
        if self.animation_index != -1:
            self.menu.screen.blit(self.click_animation[self.animation_index], (self.pos[0]-TILE_SIZE//2, self.pos[1]-TILE_SIZE//2))
        self.menu.screen.blit(self.mouse_image, self.pos)