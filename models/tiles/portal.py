from .animated_tile import *
from .tile_utils import *

class Portal(AnimatedTile):
    """Tile that teleports the player (and other entities/tiles)"""
    def __init__ (self, tile_id:str, images:list[pg.Surface], pos:tuple[int, int], link:tuple[int, int]) -> None:
        self.pos = pos
        self.link = link # refers to teleport position
        properties = construct_properties(tangible=False)
        super().__init__(tile_id, images, properties, rotation=0)