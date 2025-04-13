class Spawner:
    """*Not* a tile class. It represents a spawner tile that can spawn other tiles, but it is not responsible for drawing the actual tile"""
    def __init__ (self, tile_x:int, tile_y:int, tile_id:str, spawn_id:str, rotation:int):
        self.tile_x = tile_x
        self.tile_y = tile_y
        self.tile_id = tile_id
        self.rotation = rotation % 360 # is either 0, 90, 180 or 270
        self.spawn_id = f"{spawn_id}:{int(self.rotation/90)}"

    def object_interrupt(self, spawner:"Spawner", movables:list) -> bool:
        """Check if any objects between self and spawner such as tiles"""
        # add (in the future) a check for if other spawners interrupt

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
        """Check if a spawner can spawn tiles with self."""
        if self.tile_id != spawner.tile_id:
            return False
        
        # can't be same spawner
        if spawner.tile_x == self.tile_x and spawner.tile_y == self.tile_y:
            return False
        
        # has to face each other
        if self.rotation != (spawner.rotation - 180) % 360:
            return False
        
        # if facing each other horizontally and the y values don't match
        if self.rotation in (0, 180) and self.tile_y != spawner.tile_y:
            return False
        
        # if facing each other vertically and the x values don't match
        if self.rotation in (90, 270) and self.tile_x != spawner.tile_x:
            return False

        # true case - if in correct orientation
        if (self.rotation == 0 and self.tile_x < spawner.tile_x or
            self.rotation == 180 and self.tile_x > spawner.tile_x or 
            self.rotation == 90 and self.tile_y < spawner.tile_y or
            self.rotation == 270 and self.tile_y > spawner.tile_y):
            return not self.object_interrupt(spawner, movables)
        
        return False
    
    def get_tile_positions_hor(self, spawner:"Spawner") -> list[dict]:
        """Get all non static tile positions (horizontal)"""
        return [
            { "pos": (x, self.tile_y), "spawn_id": self.spawn_id }
            for x in range(min(self.tile_x, spawner.tile_x)+1, max(self.tile_x, spawner.tile_x))
        ]
    
    def get_tile_positions_vert(self, spawner:"Spawner") -> list[dict]:
        """Get all non static tile positions (vertical)"""
        return [
            { "pos": (self.tile_x, y), "spawn_id": self.spawn_id }
            for y in range(min(self.tile_y, spawner.tile_y)+1, max(self.tile_y, spawner.tile_y))
        ]

    def get_spawned_tiles(self, spawners:list, movables:list) -> list[int, int]:
        """Receives a list of other spawners and returns positions of tiles to be spawned"""
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