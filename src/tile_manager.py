from tile import *

class TileManager:
    def __init__ (self, map_2d:dict, tile_data:dict) -> None:
        # dictionary of tiles
        self.tile_data = tile_data
        self.tiles:dict = {}        
        for j, row in enumerate(map_2d):
            for i, tile_id in enumerate(row):
                if tile_id == "0.0.00":
                    continue
                self.tiles[(i, j)] = get_tile(tile_id, tile_data)

        self.spawners = [
            Spawner(pos[0], pos[1], self.tiles[pos].id, 
                    tile_data[self.tiles[pos].id.split(":")[0]]["spawn_id"], self.tiles[pos].rotation)
            for pos in self.tiles if self.tiles[pos].spawner
        ]

        self.movables = []
        self.non_static_tiles:dict[tuple[int, int], list] = {}

    def contains(self, tile_pos:list[int, int]) -> bool:
        return tile_pos in self.tiles

    def wall(self, tile_pos:list[int, int]) -> bool:
        if tile_pos not in self.tiles:
            return False
        
        return self.tiles[tile_pos].tangible
    
    def hazardous(self, tile_pos:list[int, int]) -> bool:
        if tile_pos not in self.tiles:
            return False
        
        return self.tiles[tile_pos].hazardous
    
    def win(self, tile_pos:list[int, int]) -> bool:
        if tile_pos not in self.tiles:
            return False
        
        return self.tiles[tile_pos].win
    
    def die(self, tile_pos:list[int, int]) -> bool:
        if tile_pos not in self.non_static_tiles:
            return False
        
        return any([tile.hazardous for tile in self.non_static_tiles[tile_pos]])
    
    def update(self) -> None:
        new_non_static_tiles:dict[tuple[int, int], list] ={}

        self.spawned_tiles = []
        for spawner in self.spawners:
            self.spawned_tiles += spawner.get_spawned_tiles(self.spawners, self.movables)

        for tile_dict in self.spawned_tiles:
            if tile_dict["pos"] not in self.non_static_tiles:
                new_non_static_tiles[tile_dict["pos"]] = [get_tile(tile_dict["spawn_id"], self.tile_data)]
            elif not any([tile_dict["spawn_id"].split(":")[0] == tile.id for tile in self.non_static_tiles[tile_dict["pos"]]]):
                new_non_static_tiles[tile_dict["pos"]].append(get_tile(tile_dict["spawn_id"], self.tile_data))
        
        # match new non static tiles and old non static tiles
        # i cannot just reset non_static_tiles every time or else the animations won't work
        for pos in new_non_static_tiles:
            if pos not in self.non_static_tiles:
                self.non_static_tiles[pos] = new_non_static_tiles[pos]
                continue
            
            # check if any tiles from old list don't appear in new list (if so then delete)
            for i, old_tile in enumerate(self.non_static_tiles[pos].copy()):
                if not any([same_tile(old_tile) == tile for tile in new_non_static_tiles[pos]]):
                    self.non_static_tiles[pos].pop(i)
            
            # check if any tiles from new list don't appear in old list (if so then add)
            for i, new_tile in enumerate(new_non_static_tiles):
                if not any([same_tile(new_tile) == tile for tile in self.non_static_tiles[pos]]):
                    self.non_static_tiles[pos].append(new_tile)

        for pos in self.tiles:
            self.tiles[pos].update()

        for pos in self.non_static_tiles:
            for tile in self.non_static_tiles[pos]:
                tile.update()

    def draw_tile(self, surface:pg.Surface, tile_pos:tuple[int, int], pixel_pos:tuple[int, int]) -> None:
        if tile_pos not in self.tiles:
            return
        surface.blit(self.tiles[tile_pos].image, pixel_pos)

    def draw_non_static(self, surface:pg.Surface, tile_pos:tuple[int, int], pixel_pos:tuple[int, int]) -> None:
        if tile_pos not in self.non_static_tiles:
            return
        
        for tile in self.non_static_tiles[tile_pos]:
            surface.blit(tile.image, pixel_pos)