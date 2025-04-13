from models.tiles.tile import *
from models.tiles.tile_utils import *

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