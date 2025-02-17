import pygame as pg

# Classic Tile - simple display/animation
class Tile:
    def __init__(self, id:str, tile_info:dict):
        self.id = id
        self.walkable = id[0] == "0"
        self.rotation = int(id.split(":")[1]) * 90

        if type(tile_info["image"]) == list:
            self.images = [pg.transform.rotate(i, -self.rotation) for i in tile_info["image"]]
        else: self.images = [pg.transform.rotate(tile_info["image"], -self.rotation)]

        self.load_images = [pg.transform.rotate(i, -self.rotation) for i in tile_info["load_images"]]
        self.load_index = 0
        self.idle_index = 0
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

# A tile that is electric - turned off and on depending on its parent nodes
class ElectricTile(Tile):
    def __init__(self, id:str, tile_info:dict, parent_nodes:list):
        super().__init__(id, tile_info)

class ElectricNode(Tile):
    def __init__(self, id:str, tile_info:dict):
        super().__init__(id, tile_info)

        self.connections = {
            "LEFT": False,
            "RIGHT": False,
            "UP": False,
            "DOWN": False
        }

# A tile that can be moved by the player
class MovableTile(Tile):
    def __init__(self, id:str, tile_info:dict):
        super().__init__(id, tile_info)

# A tile that moves on a set path
class MovingTile(Tile):
    def __init__(self, id:str, tile_info:dict):
        super().__init__(id, tile_info)

# A projectile that has all the functionalities of a classic tile
class ProjecTile(Tile): # pun intended
    def __init__(self, id:str, tile_info:dict):
        super().__init__(id, tile_info)