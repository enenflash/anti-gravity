import pygame as pg, json

pg.init()
screen_info = pg.display.Info()

HEIGHT = screen_info.current_h - 80
WIDTH = 4*HEIGHT/3

TILE_SIZE = int(HEIGHT/22)

TILE_TEXTURES_PATH = "data/textures/tile_textures.json"
MAP_PATH = input("Map Path: ")

MAP_DISP_SIZE = HEIGHT-HEIGHT%TILE_SIZE-TILE_SIZE, HEIGHT-HEIGHT%TILE_SIZE-TILE_SIZE
MAP_DISP_POS = (HEIGHT-MAP_DISP_SIZE[0])/2, (HEIGHT-MAP_DISP_SIZE[1])/2

TILE_PALETTE_SIZE = WIDTH-MAP_DISP_SIZE[0]-MAP_DISP_POS[0]-TILE_SIZE, MAP_DISP_SIZE[1]
TILE_PALETTE_POS = MAP_DISP_SIZE[0]+MAP_DISP_POS[0], MAP_DISP_POS[1]

class Tile:
    def __init__(self, tile_id:str, image:pg.Surface):
        self.id = tile_id
        self.rotation = int(tile_id.split(":")[1]) * 90
        self.image = pg.transform.rotate(image, -self.rotation)

class Movable(Tile):
    def __init__ (self, tile_id:str, image:pg.Surface, pos:tuple[int, int]) -> None:
        self.pos = pos
        super().__init__(tile_id, image)

class Portal(Tile):
    def __init__ (self, tile_id:str, image:pg.Surface, pos:tuple[int, int], link:tuple[int, int]) -> None:
        self.pos = pos
        self.link = link
        super().__init__(tile_id, image)

class MapFileManager:
    def __init__ (self, map_path:str) -> None:
        self.map_path = map_path

        with open(map_path, "r+") as file:
            self.previous_map_data = json.load(file)

        self.map_arr = self.previous_map_data["map"] if "map" in self.previous_map_data else []
        self.player_start = self.previous_map_data["player-start"] if "player-start" in self.previous_map_data else [0, 0]
        self.movables = self.previous_map_data["movables"] if "movables" in self.previous_map_data else []
        self.portals = self.previous_map_data["portals"] if "portals" in self.previous_map_data else []

    def set_map_arr(self, new_map_arr:list[list[str|list]]) -> None:
        self.map_arr = new_map_arr

    def save_map(self) -> None:
        self.previous_map_data["map"] = self.map_arr
        self.previous_map_data["player-start"] = self.player_start

        if self.movables != [] or "movables" in self.previous_map_data:
            self.previous_map_data["movables"] = self.movables
        
        if self.portals != [] or "portals" in self.previous_map_data:
            self.previous_map_data["portals"] = self.portals

        with open(MAP_PATH, 'w') as file:
            json.dump(self.previous_map_data, file, indent=4)

class Map:
    def __init__(self, ld, surface_pos:tuple[int, int], pixel_dim:tuple[int, int]):
        self.ld = ld
        self.screen = ld.screen
        self.data = ld.data
        self.previous_map_data = {}
        self.surface_pos = surface_pos
        self.surface = pg.Surface(pixel_dim)

        with open(MAP_PATH, "r+") as file:
            self.previous_map_data = json.load(file)
        
        if "map" not in self.previous_map_data:
            self.previous_map_data["map"] = []
        
        map_arr = self.previous_map_data["map"]

        self.map = {}
        for j, row in enumerate(map_arr):
            for i, tile_id in enumerate(row):
                self.map[(i, j)] = self.get_tile(tile_id)

        self.tile_pos = [0, 0]

        self.selecter_rect = (
            (self.surface.get_width() - TILE_SIZE)/2, (self.surface.get_height() - TILE_SIZE)/2, TILE_SIZE, TILE_SIZE
        )

    @property
    def tile_pos_tup(self) -> tuple[int, int]:
        return (self.tile_pos[0], self.tile_pos[1])

    def get_tile(self, tile_id:str):
        if type(tile_id) == list:
            return [Tile(i, self.data.get_image(i)) for i in tile_id]
        return Tile(tile_id, self.data.get_image(tile_id))

    def get_tile_id(self, pos:tuple[int, int]):
        if pos not in self.map:
            return self.ld.editor.tile_ids[0]
        if type(self.map[pos]) == list:
            return [i.id for i in self.map[pos]]
        return self.map[pos].id
    
    def create_tile(self, tile_id:str):
        return Tile(tile_id, self.data.get_image(tile_id))
    
    def shave_empty_tiles(self, game_map:list[list]):
        # shave of empty tiles x_min
        while all([row[0].split(":")[0] == "0.0.00" if type(row[0]) == str else False for row in game_map]):
            for j in range(len(game_map)):
                game_map[j].pop(0)

        # empty tiles x_max
        while all([row[len(game_map[0])-1].split(":")[0] == "0.0.00" if type(row[len(game_map[0])-1]) == str else False for row in game_map]):
            for j in range(len(game_map)):
                game_map[j].pop()

        # empty tiles y_min
        while all(i.split(":")[0] == "0.0.00" if type(i[0]) == str else False for i in game_map[0]):
            game_map.pop(0)

        while all(i.split(":")[0] == "0.0.00" if type(i[0]) == str else False for i in game_map[len(game_map)-1]):
            game_map.pop()

        return game_map

    def save_map(self):
        x_min = min([pos[0] for pos in self.map])
        x_max = max([pos[0] for pos in self.map])
        y_min = min([pos[1] for pos in self.map])
        y_max = max([pos[1] for pos in self.map])
        
        game_map = [[self.get_tile_id((i, j)) for i in range(x_min, x_max+1)] for j in range(y_min, y_max+1)]
        game_map = self.shave_empty_tiles(game_map)
        self.previous_map_data["map"] = game_map

        with open(MAP_PATH, 'w') as file:
            json.dump(self.previous_map_data, file, indent=4)

    def set_tile(self, pos:tuple[int, int], tile_id:str) -> None:
        self.map[pos] = Tile(tile_id, self.data.get_image(tile_id))

    def add_tile(self, pos:tuple[int, int], tile_id:str) -> None:
        if pos not in self.map:
            self.map[pos] = Tile(tile_id, self.data.get_image(tile_id))
            return
        
        if type(self.map[pos]) == list:
            self.map[pos].append(Tile(tile_id, self.data.get_image(tile_id)))
            return
        
        if id.split(":")[0] == "0.0.00":
            self.map[pos] = [Tile(tile_id, self.data.get_image(tile_id))]
            return
        
        self.map[pos] = [self.map[pos], Tile(tile_id, self.data.get_image(tile_id))]

    def clear_tile(self, pos:tuple[int, int]):
        self.map[pos] = Tile("0.0.00:0", self.data.get_image("0.0.00:0"))

    def update(self):
        if pg.K_w in self.ld.keydowns:
            self.tile_pos[1] -= 1
        elif pg.K_s in self.ld.keydowns:
            self.tile_pos[1] += 1

        if pg.K_a in self.ld.keydowns:
            self.tile_pos[0] -= 1
        elif pg.K_d in self.ld.keydowns:
            self.tile_pos[0] += 1

        if pg.K_m in self.ld.keydowns:
            self.save_map()
            print("Map Saved")

        print(f"\rpos: {self.tile_pos}", end="")
    
    def draw(self):
        self.surface.fill("BLACK")

        n_tiles_x = int(MAP_DISP_SIZE[0]/TILE_SIZE) + 2
        n_tiles_y = int(MAP_DISP_SIZE[1]/TILE_SIZE) + 2

        tile_start_x = int(self.tile_pos[0] - n_tiles_x/2) + 1
        tile_start_y = int(self.tile_pos[1] - n_tiles_y/2) + 1

        for j in range(n_tiles_y):
            for i in range(n_tiles_x):
                self.draw_tile((tile_start_x+i, tile_start_y+j), (i*TILE_SIZE, j*TILE_SIZE))
        
        pg.draw.rect(self.surface, "WHITE", (0, 0, self.surface.get_width(), self.surface.get_height()), 2)
        pg.draw.rect(self.surface, "WHITE", self.selecter_rect, 1)
        self.screen.blit(self.surface, self.surface_pos)

    def draw_tile(self, tile_pos:Tile, pixel_pos:tuple[int, int]) -> None:
        if tile_pos not in self.map:
            return
        
        if type(self.map[tile_pos]) == list:
            [self.surface.blit(tile.image, pixel_pos) for tile in self.map[tile_pos]]
            return
        
        self.surface.blit(self.map[tile_pos].image, pixel_pos)

class Data:
    def __init__(self, ld) -> None:
        self.ld = ld
        
        with open(TILE_TEXTURES_PATH) as file:
            self.tile_data = json.load(file)
        
        for i in self.tile_data:
            self.tile_data[i]["image"] = self.get_texture(self.tile_data[i]["texture"], self.tile_data[i]["type"])

    def get_texture(self, path:str, image_type:str) -> pg.Surface:
        image = pg.image.load(path).convert_alpha()
        if image_type != "image":
            image = image.subsurface((0, 0, 16, 16))
        scale = TILE_SIZE / image.get_height()
        return pg.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))
    
    def get_image(self, tile_id:str) -> pg.Surface:
        return self.tile_data[tile_id.split(":")[0]]["image"]
    
class Editor:
    def __init__(self, ld):
        self.ld = ld
        self.screen = ld.screen

        self.tile_ids = [i+":0" for i in self.ld.data.tile_data]
        self.tile_images = [self.ld.data.tile_data[i]["image"] for i in self.ld.data.tile_data]
        self.tile_index = 0

    def update(self):
        if pg.K_RIGHT in self.ld.keydowns:
            self.tile_index += 1
        if pg.K_LEFT in self.ld.keydowns:
            self.tile_index -= 1

        if self.tile_index < 0:
            self.tile_index = len(self.tile_ids) - 1
        elif self.tile_index == len(self.tile_ids):
            self.tile_index = 0

        if pg.K_r in self.ld.keydowns:
            self.tile_images[self.tile_index] = pg.transform.rotate(self.tile_images[self.tile_index], -90)
            rotation = (float(self.tile_ids[self.tile_index].split(":")[1]) * 90 + 90) % 360
            self.tile_ids[self.tile_index] = self.tile_ids[self.tile_index].split(":")[0] + ":" + str(int(rotation/90))

        if pg.K_RETURN in self.ld.keydowns:
            self.ld.map.set_tile(self.ld.map.tile_pos_tup, self.tile_ids[self.tile_index])
        if pg.K_c in self.ld.keydowns:
            self.ld.map.clear_tile(self.ld.map.tile_pos_tup)
        if pg.K_v in self.ld.keydowns:
            self.ld.map.add_tile(self.ld.map.tile_pos_tup, self.tile_ids[self.tile_index])

    def draw(self):
        pg.draw.rect(self.screen, "WHITE", (TILE_PALETTE_POS[0], TILE_PALETTE_POS[1], TILE_PALETTE_SIZE[0], TILE_PALETTE_SIZE[1]), 2)
        self.screen.blit(self.tile_images[self.tile_index], (HEIGHT-TILE_SIZE+(WIDTH-HEIGHT+TILE_SIZE)/2-TILE_SIZE/2, HEIGHT/2-TILE_SIZE/2))

class LevelDesign:
    def __init__(self):
        self.running = True

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.delta_time = 1

        self.keys = pg.key.get_pressed()
        self.keydowns = []

        self.events = pg.event.get()

        self.data = Data(self)
        self.map = Map(self, MAP_DISP_POS, MAP_DISP_SIZE)
        self.editor = Editor(self)

    def find_keydowns(self):
        keydown_events = pg.event.get(pg.KEYDOWN)
        self.keydowns = [event.key for event in keydown_events]

    def update(self):
        self.delta_time = self.clock.tick(60)

        self.keys = pg.key.get_pressed()
        self.find_keydowns()
        self.events = pg.event.get()
        
        self.map.update()
        self.editor.update()

    def draw(self):
        self.screen.fill("BLACK")

        self.map.draw()
        self.editor.draw()

        pg.display.flip()

    def run(self):
        while self.running:

            event_types = [i.type for i in self.events]
            if pg.QUIT in event_types or self.keys[pg.K_ESCAPE]:
                self.running = False

            self.update()
            self.draw()

if __name__ == "__main__":
    ld = LevelDesign()
    ld.run()
    pg.quit()
    quit()