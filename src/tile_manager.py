from src.settings import *
from models.tiles import *

class TileManager:
    """
    Manages tiles for the map class
    \nContains many utility functions for the player class and other entities to use
    \nCall update() every game loop
    \nMap calls draw_at_pos() to draw tiles at a specific position (if there are tiles there)
    """
    def __init__ (self, player:object, map_data:dict, tile_data:dict) -> None:
        self.player = player

        # dictionary of tiles
        self.tile_data = tile_data

        # normal tiles
        self.tiles:dict = {}        
        for j, row in enumerate(map_data["map"]):
            for i, tile_id in enumerate(row):
                if tile_id == "0.0.00":
                    continue
                self.tiles[(i, j)] = get_tile(tile_id, tile_data)

        self.spawners = [
            Spawner(pos[0], pos[1], self.tiles[pos].id, 
                    tile_data[self.tiles[pos].id.split(":")[0]]["spawn_id"], self.tiles[pos].rotation)
            for pos in self.tiles if self.tiles[pos].spawner
        ]

        # movables tiles
        self.movables:list[Movable] = []
        if "movables" in map_data:
            self.movables = [
                Movable(movable_dict["id"], tile_data[movable_dict["id"]]["image"], movable_dict["pos"], i)
                for i, movable_dict in enumerate(map_data["movables"])
            ]

        # portals
        self.portals:dict[tuple[int, int], Portal] = {}
        if "portals" in map_data:
            for portal_dict in map_data["portals"]:
                tile_pos = (portal_dict["pos"][0], portal_dict["pos"][1]) # turn list to tuple
                link = (portal_dict["link"][0], portal_dict["link"][1])
                self.portals[tile_pos] = Portal(portal_dict["id"], tile_data[portal_dict["id"]]["image"], tile_pos, link)

        # non static tiles (electricity)
        self.non_static_tiles:dict[tuple[int, int], list] = {}

    def contains(self, tile_pos:list[int, int]) -> bool:
        """Check if a tile position is in the map"""
        return tile_pos in self.tiles
    
    # clearly 10/10 variable names
    def unmovable_movable(self, tile_pos:list[int, int], dx:int, dy:int, movable_index:int|None=None) -> bool:
        """Check if there is a movable that cannot move at a specific location"""
        for i, movable in enumerate(self.movables):
            if i == movable_index:
                continue
            if movable.check_stuck(self.wall, self.unmovable_movable, tile_pos, dx, dy):
                return True
        return False

    def wall(self, tile_pos:list[int, int]) -> bool:    
        """Check if there is a wall at a specific position"""    
        if tile_pos not in self.tiles:
            return False
        
        return self.tiles[tile_pos].tangible
    
    def win(self, tile_pos:list[int, int]) -> bool:
        """Check if player is on the win tile"""
        if tile_pos not in self.tiles:
            return False
        
        return self.tiles[tile_pos].win
    
    def hazardous(self, tile_pos:list[int, int]) -> bool:
        """Check if the tile at a specific position is hazardous"""
        if tile_pos not in self.tiles:
            return False
        
        return self.tiles[tile_pos].hazardous
    
    def die(self, tile_pos:list[int, int]) -> bool:
        """Check if the player is on a hazardous tile (includes non-statics)"""
        if tile_pos not in self.non_static_tiles:
            return False
        
        return any([tile.hazardous for tile in self.non_static_tiles[tile_pos]]) or self.hazardous(tile_pos)
    
    def portal(self, tile_pos:list[int, int]) -> None|tuple[int, int]:
        """Check if the player is on a portal tile. If it is, return the teleport position"""
        if tile_pos not in self.portals:
            return None
        
        return self.portals[tile_pos].link
    
    def sort_new_non_static_tiles(self, new_non_static_tiles:dict[tuple[int, int], list]):
        """Sync old non static tiles list with the new non static tiles lsit"""
        # check if any tiles from old list don't appear in new list (if so then delete)
        for pos in self.non_static_tiles:
            if pos not in new_non_static_tiles:
                self.non_static_tiles[pos] = []
            for i, old_tile in enumerate(self.non_static_tiles[pos].copy()):
                if not any([same_tile(old_tile, tile) for tile in new_non_static_tiles[pos]]):
                    self.non_static_tiles[pos].pop(i)

        # clear empty lists from non static tiles
        for pos in self.non_static_tiles.copy():
            if self.non_static_tiles[pos] == []:
                del self.non_static_tiles[pos]

        for pos in new_non_static_tiles:
            # if all tiles in this position are new
            if pos not in self.non_static_tiles:
                self.non_static_tiles[pos] = new_non_static_tiles[pos]
                continue
            
            # check if any tiles from new list don't appear in old list (if so then add)
            for new_tile in new_non_static_tiles[pos]:
                if not any([same_tile(new_tile, tile) for tile in self.non_static_tiles[pos]]):
                    self.non_static_tiles[pos].append(new_tile)
    
    def update(self) -> None:
        new_non_static_tiles:dict[tuple[int, int], list] = {}

        # get all spawned tiles
        self.spawned_tiles = []
        for spawner in self.spawners:
            self.spawned_tiles += spawner.get_spawned_tiles(self.spawners, self.movables)

        # get new non static tiles
        for tile_dict in self.spawned_tiles:
            if tile_dict["pos"] not in new_non_static_tiles:
                new_non_static_tiles[tile_dict["pos"]] = [get_tile(tile_dict["spawn_id"], self.tile_data)]
            elif not any([tile_dict["spawn_id"].split(":")[0] == tile.id for tile in new_non_static_tiles[tile_dict["pos"]]]):
                new_non_static_tiles[tile_dict["pos"]].append(get_tile(tile_dict["spawn_id"], self.tile_data))

        # match new non static tiles and old non static tiles
        # i cannot just reset non_static_tiles every time or else the animations won't work
        self.sort_new_non_static_tiles(new_non_static_tiles)

        # update all tiles
        for pos in self.tiles:
            self.tiles[pos].update()

        for pos in self.non_static_tiles:
            for tile in self.non_static_tiles[pos]:
                tile.update()

        for movable in self.movables:
            movable.update(self.movables, self.wall, self.unmovable_movable, self.portal, (self.player.x, self.player.y), (self.player.dx, self.player.dy), (self.player.speed_x, self.player.speed_y))

        for pos in self.portals:
            self.portals[pos].update()
        
        # ensure movables round position to int when player stops pushing
        if not self.player.moving:
            for movable in self.movables:
                movable.round_pos()

    def draw_tile(self, surface:pg.Surface, tile_pos:tuple[int, int], pixel_pos:tuple[int, int]) -> None:
        """Draw regular tile at position"""
        if tile_pos not in self.tiles:
            return
        surface.blit(self.tiles[tile_pos].image, pixel_pos)

    def draw_non_static(self, surface:pg.Surface, tile_pos:tuple[int, int], pixel_pos:tuple[int, int]) -> None:
        """Draw all non static tiles at position"""
        # if no non-static tile at position don't draw anything
        if tile_pos not in self.non_static_tiles:
            return
        
        for tile in self.non_static_tiles[tile_pos]:
            surface.blit(tile.image, pixel_pos)

    def draw_movable(self, surface:pg.Surface, tile_pos:tuple[int, int], pixel_pos:tuple[int, int]) -> None:
        """Draw movables at a position (with an offset if it is moving)"""
        for movable in self.movables:
            if tile_pos != movable.pos:
                continue
            pixel_pos_float = pixel_pos[0]+TILE_SIZE*(movable.tile_x%1), pixel_pos[1]+TILE_SIZE*(movable.tile_y%1)
            surface.blit(movable.image, pixel_pos_float)

    def draw_portal(self, surface:pg.Surface, tile_pos:tuple[int, int], pixel_pos:tuple[int, int]) -> None:
        """Draw portals at a position"""
        if tile_pos not in self.portals:
            return
        surface.blit(self.portals[tile_pos].image, pixel_pos)

    def draw_at_pos(self, surface:pg.Surface, tile_pos:tuple[int, int], pixel_pos:tuple[int, int]) -> None:
        """Draw all tiles at a specific position"""
        self.draw_tile(surface, tile_pos, pixel_pos)
        self.draw_non_static(surface, tile_pos, pixel_pos)
        self.draw_movable(surface, tile_pos, pixel_pos)
        self.draw_portal(surface, tile_pos, pixel_pos)