import math
from settings import *

class Background:
    def __init__(self, game, screen):
        self.game = game
        self.screen = screen

        bg_path = "resources/background/space_bg.png"
        image = pg.image.load(bg_path).convert_alpha()
        scale = BG_SIZE / image.get_height()
        self.image = pg.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))

    def draw_static(self, offset:tuple=(0, 0)):

        n_tiles_x = 2*math.ceil(HALF_SCREEN_W/BG_SIZE)
        n_tiles_y = 2*math.ceil(HALF_SCREEN_H/BG_SIZE)

        tile_offset = offset

        for j in range(0, n_tiles_y + 1):
            for i in range(0, n_tiles_x + 1):
                self.screen.blit(self.image, (i*BG_SIZE+tile_offset[0]-BG_SIZE, j*BG_SIZE+tile_offset[1]-BG_SIZE))

    def draw(self):
        player_x_offset = (self.game.player.x * TILE_SIZE)/10
        player_y_offset = (self.game.player.y * TILE_SIZE)/10

        half_n_tiles_x = math.ceil((HALF_SCREEN_W - player_x_offset)/BG_SIZE)
        half_n_tiles_y = math.ceil((HALF_SCREEN_H - player_y_offset)/BG_SIZE)

        n_tiles_x = half_n_tiles_x + math.ceil((HALF_SCREEN_W + player_x_offset)/BG_SIZE)
        n_tiles_y = half_n_tiles_y + math.ceil((HALF_SCREEN_H + player_y_offset)/BG_SIZE)

        tile_offset = [-(BG_SIZE - (HALF_SCREEN_W - player_x_offset)%BG_SIZE), -(BG_SIZE - (HALF_SCREEN_H - player_y_offset)%BG_SIZE)]

        for j in range(0, n_tiles_y + 1):
            for i in range(0, n_tiles_x + 1):
                self.screen.blit(self.image, (i*BG_SIZE+tile_offset[0], j*BG_SIZE+tile_offset[1]))