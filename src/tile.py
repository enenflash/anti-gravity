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

    def update(self) -> None:
        pass

class AnimatedTile(Tile):
    def __init__ (self, tile_id:str, images:list[pg.Surface], properties:dict, rotation:int=0) -> None:
        self.images = images
        self.image_index = 0
        self.anim_delay = 4
        self.anim_time = 0
        super().__init__(tile_id, images[0], properties, rotation)

    def update(self) -> None:
        if self.anim_time == self.anim_delay:
            self.image_index = self.image_index + 1 if self.image_index < len(self.images) - 1 else 0
            self.anim_time = 0
        
        self.anim_time += 1
        self.image = self.images[self.image_index]

class StackedTile(Tile):
    """
    Multiple tiles stacked on top of each other
    """
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

class Spawner:
    def __init__ (self, tile_x:int, tile_y:int, tile_id:str, spawn_id:str, rotation:int):
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.tile_id = tile_id
        self.rotation = rotation % 360 # is either 0, 90, 180 or 270
        self.spawn_id = f"{spawn_id}:{int(self.rotation/90)}"

    def object_interrupt(self, spawner:"Spawner", movables:list) -> bool:
        return False
    
    def validate_spawner(self, spawner:"Spawner", movables:list) -> bool:
        if self.tile_id != spawner.tile_id:
            return False
        
        # if not facing each other
        if self.rotation != (spawner.rotation - 180) % 360:
            return False
        
        # if facing each other horizontally and the y values don't match
        if self.rotation in (0, 180) and self.tile_y != spawner.tile_y:
            return False
        
        # if facing each other vertically and the x values don't match
        if self.rotation in (90, 270) and self.tile_x != spawner.tile_x:
            return False
        
        if (self.rotation == 0 and self.tile_x < spawner.tile_x or
            self.rotation == 180 and self.tile_x > spawner.tile_x or 
            self.rotation == 90 and self.tile_y < spawner.tile_y or
            self.rotation == 270 and self.tile_y > spawner.tile_y):
            return not self.object_interrupt(spawner, movables)
        
        return False
    
    def get_tile_positions_hor(self, spawner:"Spawner") -> list[dict]:
        return [
            { "pos": (x, self.tile_y), "spawn_id": self.spawn_id }
            for x in range(min(self.tile_x, spawner.tile_x)+1, max(self.tile_x, spawner.tile_x))
        ]
    
    def get_tile_positions_vert(self, spawner:"Spawner") -> list[dict]:
        return [
            { "pos": (self.tile_x, y), "spawn_id": self.spawn_id }
            for y in range(min(self.tile_y, spawner.tile_y)+1, max(self.tile_y, spawner.tile_y))
        ]

    def get_spawned_tiles(self, spawners:list, movables:list) -> list[int, int]:
        """
        Receives a list of other spawners and returns positions of tiles to be spawned
        """
        valid_spawners = [
            spawner
            for spawner in spawners
            if self.validate_spawner(spawner, movables) and not (spawner.tile_x == self.tile_x and spawner.tile_y == self.tile_y)
        ]

        tile_positions = []
        for spawner in valid_spawners:
            if self.tile_y == spawner.tile_y:
                tile_positions += self.get_tile_positions_hor(spawner)
            if self.tile_x == spawner.tile_x:
                tile_positions += self.get_tile_positions_vert(spawner)

        return tile_positions
    
class Movable(Tile):
    def __init__ (self, tile_id:str, image:pg.Surface, start_pos:tuple[int, int]) -> None:
        # can be float
        self.tile_x, self.tile_y = start_pos
        properties = {
            "tangible": True,
            "hazardous": False,
            "win": False,
            "spawner": False
        }
        super().__init__(tile_id, image, properties, rotation=0)

    @property
    def pos(self) -> tuple[int, int]:
        return int(self.tile_x), int(self.tile_y)
    
    def round_pos(self) -> None:
        self.tile_x = self.pos[0]
        self.tile_y = self.pos[1]
    
    # if squished between player and wall
    def check_stuck(self, wall_at, player_pos:tuple[int, int], dx:int, dy:int) -> None:
        if self.pos != (player_pos[0]+dx, player_pos[1]+dy):
            return False
        new_pos = self.pos[0] + dx, self.pos[1] + dy
        return wall_at(new_pos)
    
    def update(self, wall_at, player_pos:tuple[float, float]) -> None:
        """
        tile manager passes wall_at() method
        """
        player_pos_int = int(player_pos[0]), int(player_pos[1])
        if player_pos_int[1] == self.pos[1]:
            # coming from left
            if player_pos_int[0] + 1 == self.pos[0] and not wall_at((int(self.tile_x)+1, int(self.tile_y))):
                self.tile_x = player_pos[0] + 2
            # coming from right
            elif player_pos_int[0] == self.pos[0] and not wall_at((int(self.tile_x)-1, int(self.tile_y))):
                self.tile_x = player_pos[0] - 1
        if player_pos_int[0] == self.pos[0]:
            # coming from top
            if player_pos_int[1] + 1 == self.pos[1] and not wall_at((int(self.tile_x), int(self.tile_y)+1)):
                self.tile_y = player_pos[1] + 2
            # coming from bottom
            elif player_pos_int[1] == self.pos[1] and not wall_at((int(self.tile_x), int(self.tile_y)-1)):
                self.tile_y = player_pos[1] - 1
    
def same_tile(tile1:Tile, tile2:Tile) -> bool:
    return tile1.id == tile2.id and tile1.rotation == tile2.rotation

def get_tile(full_tile_id:str|list, tile_datas:dict[dict]) -> Tile:
    if type(full_tile_id) == list:
        tiles = []
        for full_tile_id_element in full_tile_id:
            if full_tile_id_element == "0.0.00":
                continue
            tiles.append(get_tile(full_tile_id_element, tile_datas))
        return StackedTile(tiles)
    
    rotation = int(full_tile_id.split(":")[1])*90
    tile_id = full_tile_id.split(":")[0]

    tile_data = tile_datas[tile_id]
    properties = {
        "tangible": tile_data["tangible"],
        "hazardous": tile_data["hazardous"] if "hazardous" in tile_data else False,
        "win": tile_id.split(":")[0] == "0.1.00",
        "spawner": tile_data["spawner"] if "spawner" in tile_data else False
    }

    if type(tile_data["image"]) == list:
        return AnimatedTile(tile_id, [pg.transform.rotate(image, -rotation) for image in tile_data["image"]], properties, rotation=rotation)
    
    return Tile(tile_id, pg.transform.rotate(tile_data["image"], -rotation), properties, rotation=rotation)