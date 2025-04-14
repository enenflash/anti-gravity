from .tile import *
from .stacked_tile import *
from .animated_tile import *

def construct_properties(tangible:bool, hazardous:bool=False, win:bool=False, spawner:bool=False, portal:bool=False) -> dict:
    """Construct necessary tile properties"""
    return {
        "tangible": tangible,
        "hazardous": hazardous,
        "win": win,
        "spawner": spawner,
        "portal": portal
    }
    
def same_tile(tile1:Tile, tile2:Tile) -> bool:
    """Check if two tiles are the same."""
    return tile1.id == tile2.id and tile1.rotation == tile2.rotation

def get_tile(full_tile_id:str|list, tile_datas:dict[dict]) -> Tile:
    """Get tile (either default, stacked or animated (or both stacked and animated))"""
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