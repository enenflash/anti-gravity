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
    
    # liskov substitution principle
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

# Spawner is *not* a Tile, it represents a spawner tile that can spawn other tiles, but it is not responsible for drawing the actual tile
class Spawner:
    def __init__ (self, tile_x:int, tile_y:int, tile_id:str, spawn_id:str, rotation:int):
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.tile_id = tile_id
        self.rotation = rotation % 360 # is either 0, 90, 180 or 270
        self.spawn_id = f"{spawn_id}:{int(self.rotation/90)}"

    def object_interrupt(self, spawner:"Spawner", movables:list) -> bool:
        """
        Check if any objects between self and spawner
        """
        # if line up vertically
        if self.tile_x == spawner.tile_x:
            for movable in movables:
                if movable.pos[0] != self.tile_x:
                    continue
                if movable.pos[1] in range(min(self.tile_y, spawner.tile_y), max(self.tile_y, spawner.tile_y)):
                    return True
        # if line up horizontally
        if self.tile_y == spawner.tile_y:
            for movable in movables:
                if movable.pos[1] != self.tile_y:
                    continue
                if movable.pos[0] in range(min(self.tile_x, spawner.tile_x), max(self.tile_x, spawner.tile_x)):
                    return True
        return False
    
    def validate_spawner(self, spawner:"Spawner", movables:list) -> bool:
        if self.tile_id != spawner.tile_id:
            return False
        
        # if same spawner
        if spawner.tile_x == self.tile_x and spawner.tile_y == self.tile_y:
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

        # true case
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
            spawner for spawner in spawners
            if self.validate_spawner(spawner, movables)
        ]

        tile_positions = []
        for spawner in valid_spawners:
            if self.tile_y == spawner.tile_y:
                tile_positions += self.get_tile_positions_hor(spawner)
            if self.tile_x == spawner.tile_x:
                tile_positions += self.get_tile_positions_vert(spawner)

        return tile_positions
    
# tiles that the player can move
class Movable(Tile):
    def __init__ (self, tile_id:str, image:pg.Surface, start_pos:tuple[int, int], movable_index:int) -> None:
        # can be float
        self.tile_x, self.tile_y = start_pos
        self.last_push_dir = 0
        self.dx, self.dy = 0, 0
        self.speed_x, self.speed_y = 0, 0
        self.movable_index = movable_index
        properties = construct_properties(tangible=True)
        super().__init__(tile_id, image, properties, rotation=0)

    @property
    def pos(self) -> tuple[int, int]:
        return int(self.tile_x), int(self.tile_y)
    
    def round_pos(self) -> None:
        self.tile_x = self.pos[0]
        self.tile_y = self.pos[1]
    
    # if squished between player and wall or another movable
    def check_stuck(self, wall_at, unmovable_movable, entity_pos:tuple[int, int], dx:int, dy:int) -> None:
        if self.pos != (entity_pos[0]+dx, entity_pos[1]+dy):
            return False
        new_pos = self.pos[0] + dx, self.pos[1] + dy
        return wall_at(new_pos) or unmovable_movable(self.pos, dx, dy, self.movable_index)
    
    def get_pushed_hor(self, entity_pos:tuple[int|float, int|float], entity_dir:tuple[int, int], entity_speed:tuple[int, int]) -> None:
        # move left or move right
        if (entity_dir[0] == -1 and (entity_pos[0] >= self.tile_x+1 or self.tile_x + 1 - entity_pos[0] < 1) and entity_pos[0] + entity_speed[0] < self.tile_x+1
            or entity_dir[0] == 1 and (entity_pos[0] + 1 <= self.tile_x or entity_pos[0] + 1 - self.tile_x < 1) and entity_pos[0] + entity_speed[0] + 1 > self.tile_x):
            self.tile_x = entity_pos[0] + entity_dir[0] + entity_speed[0]
            self.last_push_dir = 0 if entity_dir[0] == 1 else 1
            self.dx = entity_dir[0]
            self.speed_x = entity_speed[0]
            return
        
        # else if not pushed at all
        self.dx, self.speed_x = 0, 0
        
    def get_pushed_ver(self, entity_pos:tuple[int|float, int|float], entity_dir:tuple[int, int], entity_speed:tuple[int, int]) -> None:
        # move up or move down
        if (entity_dir[1] == -1 and (entity_pos[1] >= self.tile_y + 1 or self.tile_y + 1 - entity_pos[1] < 1) and entity_pos[1] + entity_speed[1] < self.tile_y + 1
            or entity_dir[1] == 1 and (entity_pos[1] + 1 <= self.tile_y or entity_pos[1] + 1 - self.tile_y < 1) and entity_pos[1] + 1 + entity_speed[1] > self.tile_y):
            self.tile_y = entity_pos[1] + entity_dir[1] + entity_speed[1]
            self.last_push_dir = 2 if entity_dir[1] == 1 else 3
            self.dy = entity_dir[1]
            self.speed_y = entity_speed[1]
            return
        
        # else if not pushed at all
        self.dy, self.speed_y = 0, 0

    def get_pushed(self, wall_at, unmovable_movable, entity_pos:tuple[int|float, int|float], entity_dir:tuple[int, int], entity_speed:tuple[int, int]) -> None:
        entity_pos_int = int(entity_pos[0]), int(entity_pos[1])
        if wall_at((self.pos[0]+entity_dir[0], self.pos[1]+entity_dir[1])) or self.check_stuck(wall_at, unmovable_movable, entity_pos_int, entity_dir[0], entity_dir[1]):
            return
        # horizontally inline
        if entity_pos_int[1] == self.pos[1]:
            self.get_pushed_hor(entity_pos, entity_dir, entity_speed)
        if entity_pos_int[0] == self.pos[0]:
            self.get_pushed_ver(entity_pos, entity_dir, entity_speed)
    
    def update(self, movables:list, wall_at, unmovable_movable, portal_func, player_pos:tuple[float, float], player_dir:tuple[int, int], player_speed:tuple[int|float, int|float]) -> None:
        """
        tile manager passes wall_at() and portal_func() method
        """
        self.tile_x = round(self.tile_x, 2)
        self.tile_y = round(self.tile_y, 2)
        # get pushed by player
        self.get_pushed(wall_at, unmovable_movable, player_pos, player_dir, player_speed)
        self.tile_x = round(self.tile_x, 2)
        self.tile_y = round(self.tile_y, 2)
        for movable in movables:
            # can't get pushed by itself
            if movable.pos[0] == self.pos[0] and movable.pos[1] == self.pos[1]:
                continue
            if movable.dx != 0 or movable.dy != 0:
                self.get_pushed(wall_at, unmovable_movable, (movable.tile_x, movable.tile_y), (movable.dx, movable.dy), (movable.speed_x, movable.speed_y))

        # get teleported
        portal_link = portal_func(self.pos)
        if portal_link != None:
            self.tile_x = portal_link[0]
            self.tile_y = portal_link[1]

            # move a tiny bit in the direction is was being pushed into the portal
            # this is so the player can continue pushing it
            if self.last_push_dir == 0:
                self.tile_x += 0.1
            elif self.last_push_dir == 1:
                self.tile_x -= 0.1
            elif self.last_push_dir == 2:
                self.tile_y += 0.1
            elif self.last_push_dir == 3:
                self.tile_y -= 0.1

# tiles that teleport the player
class Portal(AnimatedTile):
    def __init__ (self, tile_id:str, images:list[pg.Surface], pos:tuple[int, int], link:tuple[int, int]) -> None:
        self.pos = pos
        self.link = link
        properties = construct_properties(tangible=False)
        super().__init__(tile_id, images, properties, rotation=0)

def construct_properties(tangible:bool, hazardous:bool=False, win:bool=False, spawner:bool=False, portal:bool=False) -> dict:
    return {
        "tangible": tangible,
        "hazardous": hazardous,
        "win": win,
        "spawner": spawner,
        "portal": portal
    }
    
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