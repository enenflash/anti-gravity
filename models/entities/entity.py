from src.settings import *
from src.sound import *

# base class for all moving entities
class Entity:
    """
    Base class for moving entities
    \nAdd moves to move_queue and call check_move_queue() to use
    \nCan be used for path-following tiles in the future
    """
    def __init__ (self, map:object, x:int, y:int, speed:int|float) -> None:
        self.map = map # map class
        self.x, self.y = x, y # current x and y

        # target x and y (position that the entity is moving towards)
        self.target_x, self.target_y = x, y

        self.SPEED = speed
        self.speed_x, self.speed_y = 0, 0 # vector components of speed

        # if currently moving
        self.moving = False

        # direction dictionary
        # 1 (up) -> x = 0, y = -1
        self.dir_dict = {
            1: (0, -1),
            2: (-1, 0),
            3: (0, 1),
            4: (1, 0)
        }

        self.dx, self.dy = 0, 0

        # moves to execute (such as LEFT, DOWN, UP, RIGHT)
        # the entity remembers the moves based on the keys pressed
        # executes each move after the entity has reached a target position
        self.move_queue = []
        self.move_queue_history:int=0

    @property
    def pos(self) -> tuple:
        """Int position of entity"""
        return (int(self.x), int(self.y))

    def validate_new_move(self, new_move:int) -> None:
        """
        Checks if new move is valid. If it is, add to move queue.
        """
        if new_move == 0: # 0 means no movement
            return False
        
        # ensures there is no movable
        dx, dy = self.dir_dict[new_move]
        if self.map.tile_manager.unmovable_movable(self.pos, dx, dy):
            return False
        
        # check if the entity is already at the target position
        # for example if there is a wall on the left and the entity tries to move left
        # accepts if the entity moves in a new direction
        if self.find_target_pos(self.x, self.y, new_move) == (self.x, self.y) and new_move == self.move_queue_history:   
            return False
        
        # if no moves currently in move queue
        if len(self.move_queue) == 0:
            return True
        
        # if the last move is exactly the same as the new move
        # entity cant move left twice
        # this specifically prevents the duck quack sound from getting spammed
        if self.move_queue[-1] != new_move:
            return True
        
        return False

    def find_target_pos(self, x:int, y:int, direction:int) -> tuple[int, int]:
        """
        find the target position -> the furthest the entity can move in a given direction before hitting a wall
        """
        dx, dy = self.dir_dict[direction]
        target_x, target_y = x, y

        while self.map.contains((target_x+dx, target_y+dy)):
            if self.map.wall_at((target_x+dx, target_y+dy)):
                break # if entity hits a wall
            
            target_x += dx
            target_y += dy

        return target_x, target_y
    
    def update_movement(self) -> None:
        """
        move entity according to speed x and y components (directional)
        \nstop when reach target position
        """
        # check if hit a movable (tile)
        if self.check_hit():
            return
        
        new_x = self.x + self.speed_x
        new_y = self.y + self.speed_y

        if (self.speed_x > 0 and new_x > self.target_x
            or self.speed_x < 0 and new_x < self.target_x
            or self.speed_y > 0 and new_y > self.target_y
            or self.speed_y < 0 and new_y < self.target_y):
            self.x = self.target_x
            self.y = self.target_y
        else:
            self.x += self.speed_x
            self.y += self.speed_y
        
        # if reached target destination
        if self.x == self.target_x and self.y == self.target_y:
            self.move_queue_history = self.move_queue.pop(0)
            self.moving = False

    def initiate_move(self, direction:int, delta_time:int) -> None:
        """
        set new target x and target y
        \nfind speed x and y components
        \nlimit speed to max speed
        """
        self.moving = True
        self.target_x, self.target_y = self.find_target_pos(int(self.x), int(self.y), direction)
        self.dx, self.dy = self.dir_dict[direction]
        self.speed_x = round(self.SPEED*delta_time * self.dx, 2)
        self.speed_y = round(self.SPEED*delta_time * self.dy, 2)

        # speed cap of 1 tile per frame
        mag = (self.speed_x**2 + self.speed_y**2)**(1/2)
        if mag > 1:
            self.speed_x /= mag
            self.speed_y /= mag

    def check_hit(self) -> bool:
        """Check if hit a movable that cannot move (prevents entity from going inside a movable)"""
        dx, dy = self.dir_dict[self.move_queue[0]]
        if self.map.tile_manager.unmovable_movable(self.pos, dx, dy):
            self.move_queue.pop(0)
            self.moving = False
            self.x = self.pos[0]
            self.y = self.pos[1]
            game_sound.play_sound("zhwoop")
            return True
        return False
            
    def check_move_queue(self, delta_time:int) -> None:
        """
        if currently moving, update movement
        \nelse if there are moves in move queue, initiate the move
        """

        if self.moving:
            self.update_movement()
            self.x = round(self.x, 2)
            self.y = round(self.y, 2)
            return
        
        self.x = round(self.x, 2)
        self.y = round(self.y, 2)
        
        if len(self.move_queue) == 0:
            self.dx, self.dy = 0, 0
            return

        self.initiate_move(self.move_queue[0], delta_time)