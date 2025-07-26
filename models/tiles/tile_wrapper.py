from .tile import *

class TileWrapper:
    """Tile wrapper that can be inherited by other tiles"""
    def __init__ (self, stored_tile:Tile) -> None:
        self.stored_tile = stored_tile
    @property
    def id(self) -> str:
        return self.stored_tile.id
    @property
    def rotation(self) -> int:
        return self.stored_tile.rotation
    @property
    def image(self) -> pg.Surface:
        return self.stored_tile.image
    @property
    def tangible(self) -> bool:
        return self.stored_tile.tangible
    @property
    def hazardous(self) -> bool:
        return self.stored_tile.hazardous
    @property
    def win(self) -> bool:
        return self.stored_tile.win
    @property
    def spawner(self) -> bool:
        return self.stored_tile.spawner
    def update(self) -> None:
        self.stored_tile.update()