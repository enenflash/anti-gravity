import pygame as pg, json

TILE_SIZE = 30
WIDTH = 900
HEIGHT = 600

TILE_TEXTURES_PATH = "data/tile_textures.json"
MAP_PATH = input("Map Path: ")

class Tile:
    def __init__(self, id, image):
        self.id = id
        self.walkable = id[0] == "0"
        self.rotation = int(id.split(":")[1]) * 90
        self.image = pg.transform.rotate(image, -self.rotation)

class Map:
    def __init__(self, ld):
        self.ld = ld
        self.screen = ld.screen
        self.data = ld.data
        self.previous_map_data = {}

        with open(MAP_PATH, "r+") as file:
            self.previous_map_data = json.load(file)
            map_arr = self.previous_map_data["map"]

        self.map = {}
        for j, row in enumerate(map_arr):
            for i, id in enumerate(row):
                self.map[(i, j)] = self.get_tile(id)

        self.tile_pos = [0, 0]

    def get_tile(self, id):
        if type(id) == list:
            return [Tile(i, self.data.get_image(i)) for i in id]
        return Tile(id, self.data.get_image(id))

    def get_tile_id(self, pos):
        if pos not in self.map:
            return self.ld.editor.tile_ids[0]
        if type(self.map[pos]) == list:
            return [i.id for i in self.map[pos]]
        return self.map[pos].id
    
    def create_tile(self, id):
        return Tile(id, self.data.get_image(id))
    
    def shave_empty_tiles(self, map):
        # shave of empty tiles x_min
        while all([row[0].split(":")[0] == "0.0.00" if type(row[0]) == str else False for row in map]):
            for j in range(len(map)):
                map[j].pop(0)

        # empty tiles x_max
        while all([row[len(map[0])-1].split(":")[0] == "0.0.00" if type(row[len(map[0])-1]) == str else False for row in map]):
            for j in range(len(map)):
                map[j].pop()

        # empty tiles y_min
        while all(i.split(":")[0] == "0.0.00" if type(i[0]) == str else False for i in map[0]):
            map.pop(0)

        while all(i.split(":")[0] == "0.0.00" if type(i[0]) == str else False for i in map[len(map)-1]):
            map.pop()

        return map

    def save_map(self):
        x_min = min([pos[0] for pos in self.map])
        x_max = max([pos[0] for pos in self.map])
        y_min = min([pos[1] for pos in self.map])
        y_max = max([pos[1] for pos in self.map])
        
        map = [[self.get_tile_id((i, j)) for i in range(x_min, x_max+1)] for j in range(y_min, y_max+1)]
        map = self.shave_empty_tiles(map)
        self.previous_map_data["map"] = map

        with open(MAP_PATH, 'w') as file:
            json.dump(self.previous_map_data, file, indent=4)

    def set_tile(self, pos, id):
        self.map[pos] = Tile(id, self.data.get_image(id))

    def add_tile(self, pos, id):
        if pos not in self.map:
            self.map[pos] = Tile(id, self.data.get_image(id))
            return None 
        
        if type(self.map[pos]) == list:
            self.map[pos].append(Tile(id, self.data.get_image(id)))
            return None
        
        if id.split(":")[0] == "0.0.00":
            self.map[pos] = [Tile(id, self.data.get_image(id))]
            return None
        
        self.map[pos] = [self.map[pos], Tile(id, self.data.get_image(id))]

    def clear_tile(self, pos, id):
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

        self.n_tiles_x = int(self.ld.level_screen_size[0]/TILE_SIZE)
        self.n_tiles_y = int(self.ld.level_screen_size[1]/TILE_SIZE)

        self.tile_start_x = int(self.tile_pos[0] - self.n_tiles_x/2)
        self.tile_start_y = int(self.tile_pos[1] - self.n_tiles_y/2)
    
    def draw(self):
        for j in range(self.n_tiles_y):
            for i in range(self.n_tiles_x):
                if (self.tile_start_x+i, self.tile_start_y+j) not in self.map:
                    continue
                self.draw_tile(self.map[(self.tile_start_x+i, self.tile_start_y+j)], (i*TILE_SIZE, j*TILE_SIZE, TILE_SIZE, TILE_SIZE))

    def draw_tile(self, tile, pos):
        if type(tile) == list:
            [self.screen.blit(i.image, pos) for i in tile]
            return None
        self.screen.blit(tile.image, pos)

class Data:
    def __init__(self, ld):
        self.ld = ld
        
        with open(TILE_TEXTURES_PATH) as file:
            self.tile_data = json.load(file)
        
        for i in self.tile_data:
            self.tile_data[i]["image"] = self.get_texture(self.tile_data[i]["texture"])

    def get_texture(self, path):
        image = pg.image.load(path).convert_alpha()
        scale = TILE_SIZE / image.get_height()
        return pg.transform.scale(image, (image.get_width() * scale, image.get_height() * scale))
    
    def get_image(self, id:str) -> object:
        return self.tile_data[id.split(":")[0]]["image"]
    
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
            self.ld.map.set_tile((self.ld.map.tile_pos[0], self.ld.map.tile_pos[1]), self.tile_ids[self.tile_index])
        if pg.K_c in self.ld.keydowns:
            self.ld.map.clear_tile((self.ld.map.tile_pos[0], self.ld.map.tile_pos[1]), self.tile_ids[self.tile_index])
        if pg.K_v in self.ld.keydowns:
            self.ld.map.add_tile((self.ld.map.tile_pos[0], self.ld.map.tile_pos[1]), self.tile_ids[self.tile_index])

    def draw(self):
        self.screen.blit(self.tile_images[self.tile_index], (735-15, 300-15))

class LevelDesign:
    def __init__(self):
        self.running = True
        self.game_state = "MENU"

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        self.delta_time = 1

        self.keys = pg.key.get_pressed()
        self.keydowns = []
        self.mouse_buttons = pg.mouse.get_pressed()

        self.events = pg.event.get()

        self.data = Data(self)
        self.map = Map(self)
        self.editor = Editor(self)

        self.level_screen_size = (540, 540)
        self.level_screen_pos = ((HEIGHT-self.level_screen_size[0])/2, (HEIGHT-self.level_screen_size[1])/2)

    def find_keydowns(self):
        keydown_events = pg.event.get(pg.KEYDOWN)
        self.keydowns = [event.key for event in keydown_events]

    def update(self):
        self.delta_time = self.clock.tick(60)

        self.keys = pg.key.get_pressed()
        self.find_keydowns()
        self.mouse_buttons = pg.mouse.get_pressed()

        self.events = pg.event.get()
        
        self.map.update()
        self.editor.update()

    def draw(self):
        self.screen.fill("BLACK")

        self.map.draw()
        pg.draw.rect(self.screen, (255, 255, 255), (self.level_screen_pos[0], self.level_screen_pos[1],
                                                    self.level_screen_size[0], self.level_screen_size[1]), 3)
        pg.draw.rect(self.screen, (255, 255, 255), (300-30, 300-30, 30, 30), 1)

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
    pg.init()
    ld = LevelDesign()
    ld.run()
    pg.quit()
    quit()