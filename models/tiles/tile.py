import pygame as pg

class Tile:
    """
    Generic tile
    \n.tile_id : 0.0.00 (no rotation)
    """
    def __init__ (self, tile_id:str, image:pg.Surface, properties:dict, rotation:int=0) -> None:
        self.id = tile_id
        self.rotation = rotation
        self.image = image
        self.tangible = properties["tangible"]
        self.hazardous = properties["hazardous"]
        self.win = properties["win"]
        self.spawner = properties["spawner"]
    
    # liskov substitution principle :P
    def update(self) -> None:
        pass