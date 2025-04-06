import pygame as pg

class Tile:
    def __init__ (self, tile_id:str, image:pg.Surface, properties:dict) -> None:
        self.id = tile_id
        self.image = image
        self.tangible = properties["tangible"]
        self.hazardous = properties["hazardous"]
        self.win = properties["win"]
        # tangible, hazardous

class StackedTile:
    def __init__ (self, tiles:list) -> None:
        self.tiles = tiles
        self.image = self.tiles[0].image
        for tile in self.tiles:
            self.image.blit(tile.image, (0, 0))
        self.tangible = any([tile.tangible for tile in self.tiles])
        self.hazardous = any([tile.hazardous for tile in self.tiles])
        self.win = any([tile.win for tile in self.tiles])

def get_rotation(tile_id:str) -> int:
    return int(tile_id.split(":")[1])*90

def get_tile(tile_id:str|list, tile_datas:dict[dict]) -> Tile:
    if type(tile_id) == list:
        tiles = []
        for tile_id_n in tile_id:
            if tile_id_n == "0.0.00":
                continue
            tiles.append(get_tile(tile_id_n, tile_datas))
        return StackedTile(tiles)
    
    rotation = get_rotation(tile_id)
    tile_data = tile_datas[tile_id.split(":")[0]]
    image = pg.transform.rotate(tile_data["image"], -rotation)
    properties = {
        "tangible": tile_data["tangible"],
        "hazardous": tile_data["hazardous"] if "hazardous" in tile_data else False,
        "win": tile_id.split(":")[0] == "0.1.00"
    }
    return Tile(tile_id, image, properties)

class TileManager:
    def __init__ (self, map_2d:dict, tile_data:dict) -> None:
        # dictionary of tiles
        self.tiles:dict = {}
        for j, row in enumerate(map_2d):
            for i, tile_id in enumerate(row):
                if tile_id == "0.0.00":
                    continue
                self.tiles[(i, j)] = get_tile(tile_id, tile_data)

    def contains(self, tile_pos:list[int, int]) -> bool:
        return tile_pos in self.tiles

    def wall_at(self, pos_x:int, pos_y:int) -> bool:
        if (pos_x, pos_y) not in self.tiles:
            return False
        
        return self.tiles[(pos_x, pos_y)].tangible
    
    def check_tile_status(self, pos:tuple[int, int]) -> str:
        if pos not in self.tiles:
            return "EMPTY"
        
        if self.tiles[pos].hazardous:
            return "HAZARDOUS"
        
        if self.tiles[pos].win:
            return "WIN"
        
        return "UNKNOWN"
    
    def update(self) -> None:
        pass
    
    def draw_tile(self, surface:pg.Surface, tile_pos:tuple[int, int], pixel_pos:tuple[int, int]) -> None:
        if tile_pos not in self.tiles:
            return
        surface.blit(self.tiles[tile_pos].image, pixel_pos)