import pygame as pg, json
from .entity import *
from src.settings import *
from src.sound import *
from src.file_loader import *

class Player(Entity):
    """Represents the player"""
    def __init__ (self, instance:object, start_x:int, start_y:int) -> None:
        self.x, self.y = start_x, start_y
        super().__init__ (instance.map, self.x, self.y, speed=0.05)
        self.instance = instance
        self.input_handler = instance.game.input_handler # shortcut
        self.animation = PlayerAnimations(self)
        
        # 0 is up, 1 is right, 2 is left, 3 is down (iirc)
        self.facing = 2
        self.last_teleported_pos = start_x, start_y

    def update(self) -> None:
        new_move = self.input_handler.get_player_movement()
        if super().validate_new_move(new_move):
            self.facing = new_move-1
            self.move_queue.append(new_move)
            game_sound.play_sound("quack")
        
        # check if player is in a portal (if so, then teleport player)
        portal_link = self.instance.map.check_portal(self.pos)
        if portal_link != None and self.pos != self.last_teleported_pos:
            game_sound.play_sound("portal")
            self.x, self.y = portal_link
            self.last_teleported_pos = portal_link
            if self.moving == False:
                self.move_queue.insert(0, self.move_queue_history)
            self.moving = False

        # last teleported pos ensures the player doesn't endlessly teleport between 2 portals
        if self.pos != self.last_teleported_pos:
            self.last_teleported_pos = (-1, -1)
        
        # update movement using entity superclass
        super().check_move_queue(self.instance.game.delta_time)

    # called by map class
    def draw(self, x_offset:int|float, y_offset:int|float, tile_start_x:int, tile_start_y:int) -> None:
        self.animation.draw((self.x-tile_start_x)*TILE_SIZE+x_offset, (self.y-tile_start_y)*TILE_SIZE+y_offset)
        
class PlayerAnimations:
    """Handles drawing the player. Will be able to handle player animations in the future."""
    def __init__ (self, player:Player) -> None:
        self.player = player
        self.surface = player.instance.surface

        self.entities = FileLoader.open_json("entity_textures.json", ENTITY_TEXTURES_PATH)
        
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