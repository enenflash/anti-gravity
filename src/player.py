import pygame as pg
from settings import *

class Player:
    def __init__(self, game):
        self.game = game
        self.screen = game.surface
        self.state = "IDLE"

        self.direction = 0
        self.move_queue = []

        self.x, self.y = 3, 3
        self.destination = 3, 3

        self.dir_dict = {
            0: (0, -1),
            1: (1, 0),
            2: (0, 1),
            3: (-1, 0)
        }

    def check_move_queue(self):
        index = 1
        while index != len(self.move_queue):
            if self.move_queue[index] == self.move_queue[index-1]:
                self.move_queue.pop(index)
            else:
                index += 1

    def initiate_animation(self, target_position, direction):
        self.destination = target_position
        self.dx = PLAYER_SPEED * direction[0]
        self.dy = PLAYER_SPEED * direction[1]
        self.state = "ANIMATING"

    def animate_movement(self):
        self.x += self.dx
        self.y += self.dy

        if (self.dx > 0 and self.x+self.dx > self.destination[0]
            or self.dx < 0 and self.x+self.dy < self.destination[0]
            or self.dy > 0 and self.y+self.dy > self.destination[1]
            or self.dy < 0 and self.y+self.dy < self.destination[1]):
            self.x = self.destination[0]
            self.y = self.destination[1]

        if self.x == self.destination[0] and self.y == self.destination[1]:
            self.state = "IDLE"
            self.move_queue.pop(0)

    def check_win(self):
        self.game.map.check_win(self.x, self.y)

    def update(self):
        self.check_win()

        if pg.K_w in self.game.keydowns or pg.K_UP in self.game.keydowns:
            self.move_queue.append(0)
        if pg.K_d in self.game.keydowns or pg.K_RIGHT in self.game.keydowns:
            self.move_queue.append(1)
        if pg.K_s in self.game.keydowns or pg.K_DOWN in self.game.keydowns:
            self.move_queue.append(2)
        if pg.K_a in self.game.keydowns or pg.K_LEFT in self.game.keydowns:
            self.move_queue.append(3)

        if self.state == "ANIMATING":
            self.animate_movement()

        if len(self.move_queue) == 0:
            return None
        
        #if len(self.move_queue) > 1:
        #    self.check_move_queue()
        
        if self.state == "IDLE":
            self.dx, self.dy = 0, 0
            dx, dy = self.dir_dict[self.move_queue[0]]
            new_position = self.find_new_position(self.x, self.y, dx, dy)
            self.initiate_animation(new_position, (dx, dy))

    def find_new_position(self, x, y, dx, dy):
        tile_walkable = True
        new_x, new_y = x, y
        while tile_walkable:
            tile_walkable = False
            if (new_x+dx, new_y+dy) in self.game.map.tiles:
                if self.game.map.walkable_tiles[(new_x+dx, new_y+dy)]:
                    tile_walkable = True
            if tile_walkable:
                new_x += dx
                new_y += dy

        return new_x, new_y

    def draw(self):
        pg.draw.circle(self.screen, "#b1ede8", (HALF_SCREEN_W, HALF_SCREEN_H), TILE_SIZE/2-2, 4)