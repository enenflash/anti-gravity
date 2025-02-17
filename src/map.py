import math, json
from settings import *
from tiles import *
import curves

class Camera:
    def __init__(self, pos):
        self.pos = pos
        self.initial_pos = pos
        self.target_pos = pos

        self.x, self.y = pos[0], pos[1]

    def get_target_pos(self, target_pos):
        self.initial_pos = self.pos
        self.target_pos = target_pos

        self.n_total_frames = math.sqrt((self.target_pos[0]-self.pos[0])**2 + (self.target_pos[1]-self.pos[1])**2)//PLAYER_SPEED
        self.current_frame = 0

    def update(self):
        self.pos = int(self.x), int(self.y)

        if self.pos == self.target_pos:
            return None
        
        self.current_frame += 1
        dx = curves.ease(self.current_frame/self.n_total_frames)
class Map:
    def __init__(self, game, map_json, map_name):
        self.game = game
        self.screen = game.surface
        self.state = "DISPLAY"

        with open("json/tile_id_v3.json") as file:
            self.tile_info = json.load(file)

        for i in self.tile_info:

            if self.tile_info[i]['type'] == "image":
                self.tile_info[i]['image'] = self.get_texture(self.tile_info[i]['texture'])
            else:
                self.tile_info[i]['image'] = self.get_images(self.tile_info[i]['texture'])

            if "load" in self.tile_info[i]:
                self.tile_info[i]['load_images'] = self.get_images(self.tile_info[i]["load"])
                continue
            
            if self.tile_info[i]['type'] == "image":
                self.tile_info[i]['load_images'] = [self.tile_info[i]['image']]
            else: self.tile_info[i]["load_images"] = self.tile_info[i]['image']

        with open(f"json/maps/{map_json}") as file:
            self.map_data = json.load(file)

        self.load_map(map_name)

        self.find_tiles()
        self.get_walkable_dict()

    def get_texture(self, path):
        image = pg.image.load(path).convert_alpha()
        #scale = TILE_SIZE // image.get_height()
        return pg.transform.scale(image, (TILE_SIZE, TILE_SIZE))
    
    def get_images(self, sprite_sheet_path):
        sprite_sheet_image = pg.image.load(sprite_sheet_path).convert_alpha()
        length = sprite_sheet_image.get_rect()[2]

        images = []
        for i in range(length//16):
            image = sprite_sheet_image.subsurface((i*16, 0, 16, 16))
            images.append(pg.transform.scale(image, (TILE_SIZE, TILE_SIZE)))

        return images
    
    def get_tile(self, id):
        if type(id) == list:
            return [Tile(i, self.tile_info[i.split(":")[0]]) for i in id]
        return Tile(id, self.tile_info[id.split(":")[0]])

    def find_tiles(self):
        self.tiles = {}
        for j, row in enumerate(self.map):
            for i, id in enumerate(row):
                self.tiles[(i, j)] = self.get_tile(id)

    def get_walkable_dict(self):
        self.walkable_tiles = {}
        for i in self.tiles:
            if type(self.tiles[i]) == list:
                self.walkable_tiles[i] = all([i.walkable for i in self.tiles[i]])
            else: self.walkable_tiles[i] = self.tiles[i].walkable

    def load_map(self, map_name):
        self.map = self.map_data[map_name]["map"]
        self.game.player.x, self.game.player.y = self.map_data[map_name]["player_start"]

    def unload_map(self):
        pass

    def check_win(self, x, y): # called by the player
        if type(self.tiles[(int(x), int(y))]) == list:
            return "0.1.00" in [i.id.split(":")[0] for i in self.tiles[(int(x), int(y))]]
        return self.tiles[(int(x), int(y))].id.split(":")[0] == "0.1.00"

    def update(self):
        for pos in self.tiles:
            if type(self.tiles[pos]) == list:
                [i.update() for i in self.tiles[pos]]
            else: self.tiles[pos].update()

    def draw(self):
        player_x_offset = (self.game.player.x % 1+0.5) * TILE_SIZE #24
        player_y_offset = (self.game.player.y % 1+0.5) * TILE_SIZE

        half_n_tiles_x = math.ceil((HALF_SCREEN_W - player_x_offset)/TILE_SIZE) #480 - 9.5 - 10
        half_n_tiles_y = math.ceil((HALF_SCREEN_H - player_y_offset)/TILE_SIZE)

        n_tiles_x = half_n_tiles_x + math.ceil((HALF_SCREEN_W + player_x_offset)/TILE_SIZE) #11
        n_tiles_y = half_n_tiles_y + math.ceil((HALF_SCREEN_H + player_y_offset)/TILE_SIZE)

        tile_offset = [-(TILE_SIZE - (HALF_SCREEN_W - player_x_offset)%TILE_SIZE), -(TILE_SIZE - (HALF_SCREEN_H - player_y_offset)%TILE_SIZE)]

        tile_start_pos = [int(self.game.player.x) - half_n_tiles_x, int(self.game.player.y) - half_n_tiles_y]
        tile_x, tile_y = tile_start_pos

        for j in range(0, n_tiles_y + 1):
            for i in range(0, n_tiles_x + 1):
                tile_pos = tile_x+i, tile_y+j

                if tile_pos not in self.tiles: continue
                
                #if self.tiles[tile_pos] == "1.00": color = (0, 200, 200)
                #else: color = (0, 50, 50)
                #pg.draw.rect(self.screen, color, (i*TILE_SIZE+tile_offset[0], j*TILE_SIZE+tile_offset[1], TILE_SIZE - 1, TILE_SIZE - 1))
                self.draw_tile(self.tiles[tile_pos], (i*TILE_SIZE+tile_offset[0], j*TILE_SIZE+tile_offset[1]))

    def draw_tile(self, tile, pos):
        if type(tile) == list:
            [self.screen.blit(i.current_image, pos) for i in tile if i.id.split(":")[0] != "0.0.00"]
            return None
        if tile.id.split(":")[0] != "0.0.00":
            self.screen.blit(tile.current_image, pos)