import pygame as pg, json
from settings import *
from entity import *
from file_loader import *

class Player(Entity):
    def __init__ (self, instance:object, start_x:int, start_y:int) -> None:
        self.x, self.y = start_x, start_y
        super().__init__ (instance.map, self.x, self.y, speed=0.05)
        self.instance = instance
        self.input_handler = instance.game.input_handler
        self.animation = PlayerAnimations(self)
        
        self.facing = 0

    def update(self) -> None:
        new_move = self.input_handler.get_player_movement()
        if super().validate_new_move(new_move):
            self.facing = new_move-1 
            self.move_queue.append(new_move)
        
        # update movement
        super().check_move_queue(self.instance.game.delta_time)

    # called by map class
    def draw(self, x_offset:int|float, y_offset:int|float, tile_start_x:int, tile_start_y:int) -> None:
        self.animation.draw((self.x-tile_start_x)*TILE_SIZE+x_offset, (self.y-tile_start_y)*TILE_SIZE+y_offset)

class PlayerAnimations:
    def __init__ (self, player:Player) -> None:
        self.player = player
        self.surface = player.instance.surface

        self.entities = FileLoader.open_json("entity_textures.json", "data/entity_textures.json")
        
        image_path = self.entities["quack"]["texture"]

        self.images = {}
        for i in range(4):
            self.images[i] = self.get_image(image_path, i)

    def get_image(self, image_path:str, rot:int):
        image = pg.image.load(image_path).convert_alpha()
        image = pg.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        return pg.transform.rotate(image, rot*90-180)

    def draw(self, screen_x:int, screen_y:int):
        self.surface.blit(self.images[self.player.facing], (screen_x, screen_y))
        #pg.draw.circle(self.surface, "WHITE", (screen_x + TILE_SIZE/2, screen_y + TILE_SIZE/2), TILE_SIZE/2, 2)