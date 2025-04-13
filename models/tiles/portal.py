from models.tiles.animated_tile import *
from models.tiles.tile_utils import *

# tiles that teleport the player
class Portal(AnimatedTile):
    def __init__ (self, tile_id:str, images:list[pg.Surface], pos:tuple[int, int], link:tuple[int, int]) -> None:
        self.pos = pos
        self.link = link
        properties = construct_properties(tangible=False)
        super().__init__(tile_id, images, properties, rotation=0)