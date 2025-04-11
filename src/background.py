import pygame as pg, math
from settings import *
from file_loader import *

class Background:
    def __init__ (self, screen:pg.Surface, bg_path:str) -> None:
        self.screen = screen
        self.surface = pg.Surface((screen_info.current_w, screen_info.current_h), pg.SRCALPHA)
        self.image = FileLoader.get_texture(bg_path, BG_SIZE, BG_SIZE)
        self.offset = [0, 0]

    def update(self) -> None:
        self.offset[0] += 0.3
        self.offset[1] += 0.3

        self.offset[0] %= BG_SIZE
        self.offset[1] %= BG_SIZE

    def draw(self) -> None:
        """
        Draw background with an offset
        """
        n_tiles_x = 2*math.ceil(screen_info.current_w/2/BG_SIZE)
        n_tiles_y = 2*math.ceil(HALF_SCREEN_H/BG_SIZE)

        tile_offset = self.offset

        for j in range(0, n_tiles_y + 1):
            for i in range(0, n_tiles_x + 1):
                self.surface.blit(self.image, (i*BG_SIZE+tile_offset[0]-BG_SIZE, j*BG_SIZE+tile_offset[1]-BG_SIZE))
        
        """
        Draw background with an offset
        """
        n_tiles_x = 2*math.ceil(screen_info.current_w/2/BG_SIZE)
        n_tiles_y = 2*math.ceil(HALF_SCREEN_H/BG_SIZE)

        tile_offset = self.offset

        for j in range(0, n_tiles_y + 1):
            for i in range(0, n_tiles_x + 1):
                self.surface.blit(self.image, (i*BG_SIZE+tile_offset[0]-BG_SIZE, j*BG_SIZE+tile_offset[1]-BG_SIZE))
        
        self.screen.blit(self.surface, (0, 0))

class DynamicBackground(Background):
    def draw(self, player_x:int|float, player_y:int|float) -> None:
        """
        Draw the background and move it according to play movements
        """
        player_x_offset = (player_x * TILE_SIZE)/10
        player_y_offset = (player_y * TILE_SIZE)/10

        half_n_tiles_x = math.ceil((HALF_SCREEN_W - player_x_offset)/BG_SIZE)
        half_n_tiles_y = math.ceil((HALF_SCREEN_H - player_y_offset)/BG_SIZE)

        n_tiles_x = half_n_tiles_x + math.ceil((HALF_SCREEN_W + player_x_offset)/BG_SIZE)
        n_tiles_y = half_n_tiles_y + math.ceil((HALF_SCREEN_H + player_y_offset)/BG_SIZE)

        tile_offset = [-(BG_SIZE - (HALF_SCREEN_W - player_x_offset)%BG_SIZE), -(BG_SIZE - (HALF_SCREEN_H - player_y_offset)%BG_SIZE)]

        for j in range(0, n_tiles_y + 1):
            for i in range(0, n_tiles_x + 1):
                self.surface.blit(self.image, (i*BG_SIZE+tile_offset[0], j*BG_SIZE+tile_offset[1]))

        self.screen.blit(self.surface, (0, 0))