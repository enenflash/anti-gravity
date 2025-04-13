import pygame as pg, json
from src.settings import *

class FileLoader:
    """
    Class for opening json files and images
    """
    @staticmethod
    def open_json(name:str, path:str) -> dict:
        try:
            with open(path) as file:
                file_dict = json.load(file)
            return file_dict
        except FileNotFoundError:
            pg.quit()
            raise FileNotFoundError(f"The file '{name}' could not be found at '{path}'. Please reinstall the default file to the correct path")
        
    def write_json(path:str, data:dict) -> dict:
        with open(path, 'w') as file:
            json.dump(data, file, indent=4)
    
    @staticmethod
    def get_raw_image(path:str) -> pg.Surface:
        return pg.image.load(path).convert_alpha()
    
    @staticmethod
    def get_texture(path:str, size_x:int=TILE_SIZE, size_y:int=TILE_SIZE) -> pg.Surface:
        image = pg.image.load(path).convert_alpha()
        return pg.transform.scale(image, (size_x, size_y))
    
    @staticmethod
    def get_textures(sprite_sheet_path:str, size_x:int=TILE_SIZE, size_y:int=TILE_SIZE, pixel_dim:int=16) -> list[pg.Surface]:
        sprite_sheet_image = pg.image.load(sprite_sheet_path).convert_alpha()
        length = sprite_sheet_image.get_rect()[2]

        images = []
        for i in range(length//pixel_dim):
            image = sprite_sheet_image.subsurface((i*pixel_dim, 0, pixel_dim, pixel_dim))
            images.append(pg.transform.scale(image, (size_x, size_y)))

        return images
    
class TileLoader(FileLoader):
    """
    Inherited from FileLoader
    \n returns tile data from json
    """
    @classmethod
    def get_tile_data(cls) -> dict:
        tile_textures = super().open_json("tile_textures.json", TILE_TEXTURES_PATH)
        tile_attributes = super().open_json("tile_attributes.json", TILE_ATTR_PATH)

        tile_info = tile_textures

        for i in tile_info:

            tile_info[i]['image'] = super().get_texture(tile_info[i]['texture']) if tile_info[i]['type'] == "image" else super().get_textures(tile_info[i]['texture'])

            tile_info[i]['tangible'] = tile_attributes[i]['tangible']
            tile_info[i]['hazardous'] = tile_attributes[i]['hazardous']

            if 'spawner' not in tile_attributes[i]:
                tile_info[i]['spawner'] = False
            else:
                tile_info[i]['spawner'] = tile_attributes[i]['spawner']

            if 'spawn_id' not in tile_attributes[i]:
                tile_info[i]['spawn_id'] = ""
            else:
                tile_info[i]['spawn_id'] = tile_attributes[i]['spawn_id']

            if "load" in tile_info[i]:
                tile_info[i]['load_images'] = super().get_textures(tile_info[i]["load"])
                continue
            
            tile_info[i]['load_images'] = [tile_info[i]['image']]

        return tile_info

class MapLoader(FileLoader):
    """
    Inherited from FileLoader
    \nreturns map data from json
    """
    @classmethod
    def get_map_data(cls, map_path:str) -> dict:
        map_data = super().open_json("map", map_path)
        return map_data
    
class MenuLoader(FileLoader):
    """
    Inherited from FileLoader
    \nreturns menu data from json
    """
    @classmethod
    def get_menu_data(cls, menu_path:str) -> dict:
        menu_data = super().open_json("menu", menu_path)
        return menu_data
    
    @classmethod
    def get_texture(cls, path:str) -> pg.Surface:
        image = super().get_raw_image(path)
        scale = image.get_height()/16*MENU_SIZE
        return pg.transform.scale(image, (image.get_width()/16*scale, image.get_height()/16*scale))
    
    @staticmethod
    def get_textures(sprite_sheet_path:str, pixel_dim:int=16) -> list[pg.Surface]:
        sprite_sheet_image = pg.image.load(sprite_sheet_path).convert_alpha()
        length = sprite_sheet_image.get_rect()[2]

        images = []
        for i in range(length//pixel_dim):
            scale = image.get_height()/16*MENU_SIZE
            image = sprite_sheet_image.subsurface((i*pixel_dim, 0, pixel_dim, pixel_dim))
            images.append(pg.transform.scale(image, (image.get_width()/16*scale, image.get_height()/16*scale)))

        return images
    
    @classmethod
    def get_element_data(cls) -> dict:
        element_textures = super().open_json("element_textures", "data/textures/element_textures.json")
        for i in element_textures:
            element = element_textures[i]
            element['image'] = cls.get_texture(element['image']) if element['type'] == "image" else cls.get_textures(element['image'])
        return element_textures
    
    @classmethod
    def get_button_data(cls) -> dict:
        button_textures = super().open_json("button_textures", "data/textures/button_textures.json")
        for i in button_textures:
            button_textures[i]['static-image'] = cls.get_texture(button_textures[i]['static']) if button_textures[i]['type'] == "image" else cls.get_textures(button_textures[i]['static'])
            button_textures[i]['selected-image'] = cls.get_texture(button_textures[i]['selected']) if button_textures[i]['type'] == "image" else cls.get_textures(button_textures[i]['selected'])
        return button_textures