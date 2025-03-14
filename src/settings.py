import pygame as pg

pg.init()
screen_info = pg.display.Info()

FPS = 60

SCREEN_W, SCREEN_H = 4*screen_info.current_h/3, screen_info.current_h
HALF_SCREEN_W, HALF_SCREEN_H = SCREEN_W/2, SCREEN_H/2

TILE_SIZE = screen_info.current_h / 21 + 0.01
BG_SIZE = screen_info.current_h / 2

PLAYER_SPEED = 0.8
CAM_SPEED = 0.4

VOLUME = 100

TILE_TEXTURES_PATH = "data/tile_textures.json"
TILE_ATTR_PATH = "data/fixed/tile_attributes.json"