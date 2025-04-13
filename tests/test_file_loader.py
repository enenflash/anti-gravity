import pygame as pg
import pygame.locals
pg.init()
screen = pygame.display.set_mode((800, 600)) # prevents pygame errors

from file_loader import *

# using entity_textures.json
def test_file_loader_open_json():
    assert type(FileLoader.open_json("entity_textures.json", "data/entity_textures.json")) == dict, "FileLoader.open_json should return dict"

# using quack.png
def test_file_loader_get_texture():
    assert type(FileLoader.get_texture("resources/entities/quack.png"))==pg.Surface, "FileLoader.get_texture should return pg.Surface"

# using the electricity sprite sheet
def test_file_loader_get_textures():
    assert type(FileLoader.get_textures("resources/tiles/sprite_sheets/electricity.png"))==list, "FileLoader.get_textures should return a list of pg.Surface"

def test_tile_loader_get_tile_data():
    assert type(TileLoader.get_tile_data())==dict, "TileLoader.get_tile_data should return a dictionary of tiles"

# using new_map.json
def test_map_loader_get_map_data():
    assert type(MapLoader.get_map_data("new_map.json"))==dict, "MapLoader.get_map_data should return a dictionary of the map"