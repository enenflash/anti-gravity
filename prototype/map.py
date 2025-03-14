import json, math

from settings import *
from tiles import *

class Map:
    def __init__ (self, instance:object, map_path:str) -> None:
        self.instance = instance
        self.surface = instance.surface

        with open(TILE_TEXTURES_PATH) as file:
            tile_textures = json.load(file)

        with open(TILE_ATTR_PATH) as file:
            tile_attributes = json.load(file)

        self.tile_info = tile_textures # dictionary of dictionaries (tiles)

        for i in self.tile_info:

            self.tile_info[i]['image'] = self.get_texture(self.tile_info[i]['texture']) if self.tile_info[i]['type'] == "image" else self.get_images(self.tile_info[i]['texture'])

            self.tile_info[i]['tangible'] = tile_attributes[i]['tangible']
            self.tile_info[i]['hazardous'] = tile_attributes[i]['hazardous']

            if "load" in self.tile_info[i]:
                self.tile_info[i]['load_images'] = self.get_images(self.tile_info[i]["load"])
                continue
            
            self.tile_info[i]['load_images'] = [self.tile_info[i]['image']]

        with open(map_path) as file:
            self.map_data = json.load(file)

        self.tiles = self.get_tiles(self.map_data["map"])
        self.player_start_x, self.player_start_y = self.map_data["player_start"]
    
    def set_up_camera(self) -> None:
        self.camera = Camera(self.instance.player, self.player_start_x, self.player_start_y)

    def get_texture(self, path:str) -> pg.SurfaceType:
        image = pg.image.load(path).convert_alpha()
        return pg.transform.scale(image, (TILE_SIZE, TILE_SIZE))

    def get_images(self, sprite_sheet_path:str) -> list[pg.SurfaceType]:
        sprite_sheet_image = pg.image.load(sprite_sheet_path).convert_alpha()
        length = sprite_sheet_image.get_rect()[2]

        images = []
        for i in range(length//16):
            image = sprite_sheet_image.subsurface((i*16, 0, 16, 16))
            images.append(pg.transform.scale(image, (TILE_SIZE, TILE_SIZE)))

        return images
    
    def get_tile(self, id:str|list) -> Tile:
        if type(id) == list:
            return StackedTile(id, [self.tile_info[i.split(":")[0]] for i in id])
        return Tile(id, self.tile_info[id.split(":")[0]])
    
    def get_tiles(self, map:list[list]) -> dict:
        tiles = {}
        for j, row in enumerate(map):
            for i, id in enumerate(row):
                if id == "0.0.00":
                    continue
                tiles[(i, j)] = self.get_tile(id)
        return tiles
    
    def check_win(self):
        func = lambda px, py, tiles: "0.1.00" in tiles[(px, py)].id
        return self.instance.player.check_for_tile(func, self.tiles)

    def update(self) -> None:
        for pos in self.tiles:
            if type(self.tiles[pos]) == list:
                [i.update() for i in self.tiles[pos]]
            else: self.tiles[pos].update()

        self.camera.update()

        if self.check_win():
            self.instance.game.sound.play_sound("victory")
            self.instance.end_instance()

    def draw(self) -> None:
        camera_offset = (self.camera.x % 1 + 0.5) * TILE_SIZE, (self.camera.y % 1 + 0.5) * TILE_SIZE

        half_n_tiles_x = math.ceil((HALF_SCREEN_W - camera_offset[0])/TILE_SIZE)
        half_n_tiles_y = math.ceil((HALF_SCREEN_H - camera_offset[1])/TILE_SIZE)

        n_tiles_x = half_n_tiles_x + math.ceil((HALF_SCREEN_W + camera_offset[0])/TILE_SIZE)
        n_tiles_y = half_n_tiles_y + math.ceil((HALF_SCREEN_H + camera_offset[1])/TILE_SIZE)

        tile_offset = [-(TILE_SIZE - (HALF_SCREEN_W - camera_offset[0])%TILE_SIZE), -(TILE_SIZE - (HALF_SCREEN_H - camera_offset[1])%TILE_SIZE)]

        tile_start_x, tile_start_y = int(self.camera.x) - half_n_tiles_x, int(self.camera.y) - half_n_tiles_y

        for j in range(0, n_tiles_y + 1):
            for i in range(0, n_tiles_x + 1):
                tile_pos = tile_start_x+i, tile_start_y+j

                if tile_pos not in self.tiles: continue
                
                #if self.tiles[tile_pos] == "1.00": color = (0, 200, 200)
                #else: color = (0, 50, 50)
                #pg.draw.rect(self.screen, color, (i*TILE_SIZE+tile_offset[0], j*TILE_SIZE+tile_offset[1], TILE_SIZE - 1, TILE_SIZE - 1))
                self.draw_tile(self.tiles[tile_pos], (i*TILE_SIZE+tile_offset[0], j*TILE_SIZE+tile_offset[1]))

        self.instance.player.draw(tile_offset[0], tile_offset[1], tile_start_x, tile_start_y)

    def draw_tile(self, tile:Tile, pos:tuple):
        if type(tile) == list:
            [self.surface.blit(i.current_image, pos) for i in tile if i.id.split(":")[0] != "0.0.00"]
            return None
        self.surface.blit(tile.current_image, pos)

class Camera:
    def __init__ (self, player:object, x:int, y:int) -> None:
        self.player = player
        self.x, self.y = x, y
        self.target_x, self.target_y = x, y
        self.speed = 0.4

    def update(self) -> None:
        if self.x == self.player.x and self.y == self.player.y:
            return

        self.target_x = self.player.x
        self.target_y = self.player.y

        p_vector = self.target_x - self.x, self.target_y - self.y
        p_vector_mag = (p_vector[0]**2 + p_vector[1]**2)**(1/2)
        scalar = self.speed/p_vector_mag

        if abs(self.player.x - self.x) < self.speed:
            self.x = self.player.x
        else:
            self.x += p_vector[0]*scalar
        
        if abs(self.player.y - self.y) < self.speed:
            self.y = self.player.y
        else:
            self.y += p_vector[1]*scalar