import math
from settings import *
from tile import *
from file_loader import *

class Map:
    def __init__ (self, instance: object, map_path:str) -> None:
        self.instance = instance
        self.surface = instance.surface

        self.tile_data = TileLoader.get_tile_data()
        self.map_data = MapLoader.get_map_data(map_path)

        self.tiles:list[Tile] = get_tiles(self.map_data["map"], self.tile_data)
        self.player_start_x, self.player_start_y = self.map_data["player_start"]

    def set_up_camera(self) -> None:
        """This function **must** be called after 'Player' is created"""
        self.camera = Camera(self.instance.player, self.player_start_x, self.player_start_y)

    #def check_win(self):
    #    func = lambda px, py, tiles: "0.1.00" in tiles[(px, py)].id
    #    return self.instance.player.check_for_tile(func, self.tiles)
    
    def update(self) -> None:
        for pos in self.tiles:
            if type(self.tiles[pos]) == list:
                [i.update() for i in self.tiles[pos]]
            else: self.tiles[pos].update()

        self.camera.update()

        #if self.check_win():
        #    print("won")

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
                self.tiles[tile_pos].draw(self.surface, (i*TILE_SIZE+tile_offset[0], j*TILE_SIZE+tile_offset[1]))
                # self.draw_tile(self.tiles[tile_pos], (i*TILE_SIZE+tile_offset[0], j*TILE_SIZE+tile_offset[1]))

        self.instance.player.draw(tile_offset[0], tile_offset[1], tile_start_x, tile_start_y)

    def draw_tile(self, tile:Tile, pos:tuple):
        if type(tile) == list:
            [self.surface.blit(i.current_image, pos) for i in tile if i.id.split(":")[0] != "0.0.00"]
            return None
        self.surface.blit(tile.current_image, pos)

class Camera:
    def __init__ (self, player:object, start_x:int, start_y:int) -> None:
        self.player = player
        self.x, self.y = start_x, start_y
        self.target_x, self.target_y = start_x, start_y
        self.speed = CAM_SPEED

    def update(self) -> None:
        self.target_x, self.target_y = self.player.x, self.player.y
        if self.x == self.target_x and self.y == self.target_y:
            return
        
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