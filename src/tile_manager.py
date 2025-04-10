from settings import *
from tile import *

class TileManager:
    def __init__ (self, player:object, map_data:dict, tile_data:dict) -> None:
        self.player = player
        # dictionary of tiles
        self.tile_data = tile_data
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
                Movable(movable_dict["id"], tile_data[movable_dict["id"]]["image"], movable_dict["pos"])
                for movable_dict in map_data["movables"]
            ]

        # portals
        self.portals:dict[tuple[int, int], Portal] = {}
        if "portals" in map_data:
            for portal_dict in map_data["portals"]:
                tile_pos = (portal_dict["pos"][0], portal_dict["pos"][1]) # turn list to tuple
                link = (portal_dict["link"][0], portal_dict["link"][1])
                self.portals[tile_pos] = Portal(portal_dict["id"], tile_data[portal_dict["id"]]["image"], tile_pos, link)

        # non static tiles
        self.non_static_tiles:dict[tuple[int, int], list] = {}

    def contains(self, tile_pos:list[int, int]) -> bool:
        return tile_pos in self.tiles

    def wall(self, tile_pos:list[int, int], dx:int|None=None, dy:int|None=None) -> bool:
        if dx != None and dy != None:
            if any([movable.check_stuck(self.wall, self.player.pos, dx, dy) for movable in self.movables]):
                return True
        
        if tile_pos not in self.tiles:
            return False
        
        return self.tiles[tile_pos].tangible
    
    def win(self, tile_pos:list[int, int]) -> bool:
        if tile_pos not in self.tiles:
            return False
        
        return self.tiles[tile_pos].win
    
    def hazardous(self, tile_pos:list[int, int]) -> bool:
        if tile_pos not in self.tiles:
            return False
        
        return self.tiles[tile_pos].hazardous
    
    def die(self, tile_pos:list[int, int]) -> bool:
        if tile_pos not in self.non_static_tiles:
            return False
        
        return any([tile.hazardous for tile in self.non_static_tiles[tile_pos]]) or self.hazardous(tile_pos)
    
    def portal(self, tile_pos:list[int, int]) -> None|tuple[int, int]:
        if tile_pos not in self.portals:
            return None
        
        return self.portals[tile_pos].link
    
    def sort_new_non_static_tiles(self, new_non_static_tiles:dict[tuple[int, int], list]):
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
            movable.update(self.wall, self.portal, self.player.pos)

        for pos in self.portals:
            self.portals[pos].update()
        
        # ensure movables round position when player stops pushing
        if not self.player.moving:
            for movable in self.movables:
                movable.round_pos()

    # called by map class
    def draw_tile(self, surface:pg.Surface, tile_pos:tuple[int, int], pixel_pos:tuple[int, int]) -> None:
        if tile_pos not in self.tiles:
            return
        surface.blit(self.tiles[tile_pos].image, pixel_pos)

    # called by map class
    def draw_non_static(self, surface:pg.Surface, tile_pos:tuple[int, int], pixel_pos:tuple[int, int]) -> None:
        # if no non-static tile at position don't draw anything
        if tile_pos not in self.non_static_tiles:
            return
        
        for tile in self.non_static_tiles[tile_pos]:
            surface.blit(tile.image, pixel_pos)

    def draw_movable(self, surface:pg.Surface, tile_pos:tuple[int, int], pixel_pos:tuple[int, int]) -> None:
        for movable in self.movables:
            if tile_pos != movable.pos:
                continue
            pixel_pos_float = pixel_pos[0]+TILE_SIZE*(movable.tile_x%1), pixel_pos[1]+TILE_SIZE*(movable.tile_y%1)
            surface.blit(movable.image, pixel_pos_float)

    def draw_portal(self, surface:pg.Surface, tile_pos:tuple[int, int], pixel_pos:tuple[int, int]) -> None:
        if tile_pos not in self.portals:
            return
        surface.blit(self.portals[tile_pos].image, pixel_pos)

    def draw_at_pos(self, surface:pg.Surface, tile_pos:tuple[int, int], pixel_pos:tuple[int, int]) -> None:
        self.draw_tile(surface, tile_pos, pixel_pos)
        self.draw_non_static(surface, tile_pos, pixel_pos)
        self.draw_movable(surface, tile_pos, pixel_pos)
        self.draw_portal(surface, tile_pos, pixel_pos)