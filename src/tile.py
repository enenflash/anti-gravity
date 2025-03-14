import pygame as pg

# every tile has an id, rotation and a set of images or just one image (and sometimes load_images)
# (i made this as generic as possible while still being practical)
class GenericTile:
    def __init__ (self, id, rotation:int, images:list, load_images:list=[]) -> None:
        """rotation: 0, 90, 180, 270 degrees"""
        if rotation not in (0, 90, 180, 270):
            print(f"tile of ID {id} has incorrect rotation format")
            rotation = 0
        self.id = id
        self.images = [pg.transform.rotate(image, -rotation) for image in images]
        self.load_images = [pg.transform.rotate(image, -rotation) for image in load_images]
        self.index = 0
        self.loading = False if self.load_images == None else True
        self.animation_delay, self.animation_time = 3, 0
        self.current_image = self.images[0] if self.loading else self.load_images[0]

    def load_tile(self):
        self.current_image = self.load_images[self.index]

        if self.index == len(self.load_images) - 1:
            self.index = 0
            self.loading = False
            return

        self.animation_time += 1
        if self.animation_time == self.animation_delay:
            self.index += 1
            self.animation_time = 0

    def update(self) -> None:
        if self.loading:
            self.load_tile()
            return None
        
        self.current_image = self.images[self.index]
        if self.index == len(self.images) - 1:
            self.index = 0
            return None
        self.index += 1

    def draw(self, surface, pos) -> None:
        surface.blit(self.current_image, pos)

# creates a generic tile based on a tile_info dictionary passed by the map class
class Tile(GenericTile):
    def __init__ (self, id:str, tile_info:dict) -> None:
        images = [tile_info["image"]] if type(tile_info['image']) != list else tile_info['image']
        super().__init__(id, rotation=int(id.split(":")[1])*90, images=images, load_images=tile_info["load_images"])
        self.tangible = tile_info['tangible']
        self.hazardous = tile_info['hazardous']

# draws multiple tiles on top of each other
class StackedTile:
    def __init__ (self, ids:list[str], tile_infos:list[dict]) -> None:
        self.id = ""
        self.tiles = []
        for i, id in enumerate(ids):
            self.tiles.append(Tile(id, tile_infos[i]))
        
        self.tangible = any([tile.tangible] for tile in self.tiles)
        self.hazardous = any([tile.hazardous for tile in self.tiles])

        self.current_image = self.tiles[0].current_image
            
    def update(self) -> None:
        for tile in self.tiles:
            tile.update()

        self.current_image = self.tiles[0].current_image
        for tile in self.tiles[1:]:
            self.current_image.blit(tile.current_image, (0, 0))

    def draw(self, surface:pg.Surface, pos:tuple) -> None:
        for tile in self.tiles:
            tile.draw(surface, pos)

def get_tile(id:str|list, tile_data:dict) -> Tile:
    if type(id) == list:
        return StackedTile(id, [tile_data[i.split(":")[0]] for i in id])
    return Tile(id, tile_data[id.split(":")[0]])

def get_tiles(map:list[list], tile_data:dict) -> dict:
    tiles = {}
    for j, row in enumerate(map):
        for i, id in enumerate(row):
            if id == "0.0.00":
                continue
            tiles[(i, j)] = get_tile(id, tile_data)
    return tiles