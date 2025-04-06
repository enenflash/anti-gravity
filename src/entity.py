from settings import *

# base class for all moving entities
class Entity:
    """
    Base class for moving entities
    \nAdd moves to move_queue and call check_move_queue() to use
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

        # moves to execute (such as LEFT, DOWN, UP, RIGHT)
        # the entity remembers the moves based on the keys pressed
        # executes each move after the entity has reached a target position
        self.move_queue = []

    @property
    def pos(self) -> tuple:
        return (int(self.x), int(self.y))

    def validate_new_move(self, new_move:int) -> None:
        """
        Checks if new move is valid. If it is, add to move queue.
        """
        if new_move == 0: # 0 means no movement
            return False
        
        # check if the entity is already at the target position
        # for example if there is a wall on the left and the entity tries to move left
        if not self.find_target_pos(self.x, self.y, new_move) != (self.x, self.y):
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
            self.move_queue.pop(0)
            self.moving = False

    def initiate_move(self, dir:int, delta_time:int) -> None:
        """
        set new target x and target y
        \nfind speed x and y components
        \nlimit speed to max speed
        """
        self.moving = True
        self.target_x, self.target_y = self.find_target_pos(int(self.x), int(self.y), dir)
        self.speed_x = self.SPEED*delta_time * self.dir_dict[dir][0]
        self.speed_y = self.SPEED*delta_time * self.dir_dict[dir][1]

        # speed cap of 1 tile per frame
        mag = (self.speed_x**2 + self.speed_y**2)**(1/2)
        if mag > 1:
            print("a")
            self.speed_x /= mag
            self.speed_y /= mag

    def check_move_queue(self, delta_time:int) -> None:
        """
        if currently moving, update movement
        \nelse if there are moves in move queue, initiate the move
        """
        if self.moving:
            self.update_movement()
            return
        
        if len(self.move_queue) == 0:
            return
        
        self.initiate_move(self.move_queue[0], delta_time)