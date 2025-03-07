import pygame as pg

class Tile:
    def __init__ (self, id:str, tile_info:dict) -> None:
        self.id = id
        self.tangible = tile_info['tangible']
        self.hazardous = tile_info['hazardous']
        self.rotation = int(id.split(":")[1]) * 90

        if type(tile_info["image"]) == list:
            self.images = [pg.transform.rotate(i, -self.rotation) for i in tile_info["image"]]
        else: self.images = [pg.transform.rotate(tile_info["image"], -self.rotation)]

        self.load_images = [pg.transform.rotate(i, -self.rotation) for i in tile_info["load_images"]]
        self.load_index, self.idle_index = 0, 0
        self.animation_delay, self.anim_time = 3, 0
        self.current_image = self.load_images[0]

    def load_tile(self):
        if self.load_index < len(self.load_images) - 1 and self.load_index != -1:
            self.anim_time += 1
            if self.anim_time == self.animation_delay:
                self.load_index += 1
                self.anim_time = 0
        else: self.load_index = -1
        
        self.current_image = self.load_images[self.load_index]

    def update(self):
        if self.load_index != -1:
            self.load_tile()
            return None
        
        self.current_image = self.images[self.idle_index]
        if self.idle_index < len(self.images) - 1:
            self.idle_index += 1
        else: self.idle_index = 0

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

    def draw(self) -> None:
        for tile in self.tiles:
            tile.draw()