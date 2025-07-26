import pygame as pg
from dataclasses import dataclass

@dataclass
class TileProperties:
    tangible: bool
    hazardous: bool
    win: bool
    spawner: bool
    responsive: bool

class Tile:
    """
    Generic tile
    \n.tile_id : 0.0.00 (no rotation)
    """
    def __init__ (self, tile_id:str, image:pg.Surface, properties:TileProperties, rotation:int=0) -> None:
        self.id = tile_id
        self.rotation = rotation
        self.image = image
        self.tangible = properties.tangible
        self.hazardous = properties.hazardous
        self.win = properties.win
        self.spawner = properties.spawner
        self.responsive = properties.responsive
    
    # liskov substitution principle :P
    def update(self) -> None:
        pass

    @staticmethod
    def construct_properties(tangible:bool, hazardous:bool=False, win:bool=False, spawner:bool=False, responsive:bool=False) -> dict:
        """Construct necessary tile properties"""
        return TileProperties(tangible=tangible, hazardous=hazardous, win=win, spawner=spawner, responsive=responsive)