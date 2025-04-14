from .tile import *

class StackedTile(Tile):
    """Multiple tiles stacked on top of each other."""
    def __init__ (self, tiles:list) -> None:
        self.tiles = tiles

        image = tiles[0].image
        for tile in tiles[1:]:
            image.blit(tile.image, (0, 0))
        
        properties = {
            "tangible": any([tile.tangible for tile in self.tiles]),
            "hazardous": any([tile.hazardous for tile in self.tiles]),
            "win": any([tile.win for tile in self.tiles]),
            "spawner": any([tile.spawner for tile in self.tiles])
        }

        super().__init__ ("", image, properties, rotation=0)

    def update(self) -> None:
        for tile in self.tiles:
            tile.update()

        self.image = self.tiles[0].image
        for tile in self.tiles[1:]:
            self.image.blit(tile.image, (0, 0))