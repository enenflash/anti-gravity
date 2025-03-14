import pygame as pg, json
from settings import *

class FileLoader:
    @staticmethod
    def open_json(name:str, path:str) -> dict:
        try:
            with open(path) as file:
                file_dict = json.load(file)
            return file_dict
        except FileNotFoundError:
            pg.quit()
            raise FileNotFoundError(f"file {name} could not be found on {path}. please reinstall the default file to the correct path")
    @staticmethod
    def get_texture(path:str) -> pg.SurfaceType:
        image = pg.image.load(path).convert_alpha()
        return pg.transform.scale(image, (TILE_SIZE, TILE_SIZE))
    @staticmethod
    def get_textures(sprite_sheet_path:str, pixel_dim:int=16) -> list[pg.SurfaceType]:
        sprite_sheet_image = pg.image.load(sprite_sheet_path).convert_alpha()
        length = sprite_sheet_image.get_rect()[2]

        images = []
        for i in range(length//pixel_dim):
            image = sprite_sheet_image.subsurface((i*pixel_dim, 0, pixel_dim, pixel_dim))
            images.append(pg.transform.scale(image, (TILE_SIZE, TILE_SIZE)))

        return images
    
class TileLoader(FileLoader):
    @classmethod
    def get_tile_data(cls) -> dict:
        tile_textures = super().open_json("tile_textures.json", TILE_TEXTURES_PATH)
        tile_attributes = super().open_json("tile_attributes.json", TILE_ATTR_PATH)

        tile_info = tile_textures

        for i in tile_info:

            tile_info[i]['image'] = super().get_texture(tile_info[i]['texture']) if tile_info[i]['type'] == "image" else super().get_textures(tile_info[i]['texture'])

            tile_info[i]['tangible'] = tile_attributes[i]['tangible']
            tile_info[i]['hazardous'] = tile_attributes[i]['hazardous']

            if "load" in tile_info[i]:
                tile_info[i]['load_images'] = super().get_textures(tile_info[i]["load"])
                continue
            
            tile_info[i]['load_images'] = [tile_info[i]['image']]

        return tile_info

class MapLoader(FileLoader):
    @classmethod
    def get_map_data(cls, map_path:str) -> dict:
        map_data = super().open_json("map", map_path)
        return map_data