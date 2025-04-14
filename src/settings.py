import pygame as pg

pg.init()
screen_info = pg.display.Info()

FPS = 60

SCREEN_W, SCREEN_H = 4*screen_info.current_h/3, screen_info.current_h
HALF_SCREEN_W, HALF_SCREEN_H = SCREEN_W/2, SCREEN_H/2

TILE_SIZE = round(screen_info.current_h / 21 + 0.01)
BG_SIZE = round(screen_info.current_h / 1.5)
MENU_SIZE = round(screen_info.current_h / 13)

PLAYER_SPEED = 0.8
CAM_SPEED = 0.2

VOLUME = 100

# DATA FILE PATHS
KEYBINDS_PATH = "data/keybinds.json"
SOUND_DATA_PATH = "data/sound.json"
PLAYER_DATA_PATH = "data/player-data/player_data.json"
LEVEL_DATA_PATH = "data/fixed/levels.json"
TILE_ATTR_PATH = "data/fixed/tile_attributes.json"

# TEXTURE FILE PATHS
ELEMENT_TEXTURES_PATH = "data/textures/element_textures.json"
BUTTON_TEXTURES_PATH = "data/textures/button_textures.json"
LEVEL_BUTTONS_PATH = "data/textures/level_buttons.json"
TILE_TEXTURES_PATH = "data/textures/tile_textures.json"
ENTITY_TEXTURES_PATH = "data/textures/entity_textures.json"