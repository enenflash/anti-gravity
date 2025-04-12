import math
from settings import *
from tile import *
from tile_manager import *
from file_loader import *

class MapText:
    def __init__ (self, text:str, tile_pos:tuple[int, int]) -> None:
        self.text = text
        self.tile_pos = tile_pos

class Map:
    def __init__ (self, instance:object, map_path:str) -> None:
        self.instance = instance
        self.surface = instance.surface

        self.tile_data = TileLoader.get_tile_data()
        self.map_data = MapLoader.get_map_data(map_path)

        self.player_start_x, self.player_start_y = self.map_data["player-start"]

    def set_up(self) -> None:
        """This function **must** be called after 'Player' is created"""
        self.camera = Camera(self.instance.player, self.player_start_x, self.player_start_y)
        self.tile_manager = TileManager(self.instance.player, self.map_data, self.tile_data)

    def contains(self, tile_pos:tuple[int, int]) -> bool:
        return self.tile_manager.contains(tile_pos)

    def wall_at(self, tile_pos:tuple[int, int]) -> bool:
        return self.tile_manager.wall(tile_pos)

    def check_win(self) -> bool:
        return self.tile_manager.win(self.instance.player.pos)
    
    def check_die(self) -> bool:
        return self.tile_manager.die(self.instance.player.pos)

    def check_portal(self, tile_pos:tuple[int, int]) -> None|tuple[int, int]:
        """
        Returns none if no portal at location
        Returns portal link if there is a portal
        """
        return self.tile_manager.portal(tile_pos)
    
    def update(self) -> None:
        self.tile_manager.update()
        self.camera.update()

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
                self.tile_manager.draw_at_pos(self.surface, tile_pos=(tile_start_x+i, tile_start_y+j), pixel_pos=(i*TILE_SIZE+tile_offset[0], j*TILE_SIZE+tile_offset[1]))

        self.instance.player.draw(tile_offset[0], tile_offset[1], tile_start_x, tile_start_y)


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
        # linear speed equation ax + a -> ease in ease out camera displacement from player
        scalar = self.speed*(p_vector_mag/20)+self.speed

        self.x += p_vector[0]*scalar
        self.y += p_vector[1]*scalar