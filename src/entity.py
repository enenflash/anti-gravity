from settings import *
# base class for all moving entities

class Entity:
    def __init__ (self, map:object, x:int, y:int, speed:int|float) -> None:
        self.map = map
        self.x, self.y = x, y
        self.target_x, self.target_y = x, y
        self.SPEED = speed
        self.speed_x, self.speed_y = 0, 0

        self.moving = False

        self.dir_dict = {
            1: (0, -1),
            2: (-1, 0),
            3: (0, 1),
            4: (1, 0)
        }

        self.move_queue = []

    @property
    def pos(self) -> tuple:
        return (int(self.x), int(self.y))

    def validate_new_move(self, new_move:int) -> None:
        if new_move == 0:
            return False
        
        if not self.find_target_pos(self.x, self.y, new_move) != (self.x, self.y):
            return False
        
        if len(self.move_queue) == 0:
            return True
        
        if self.move_queue[-1] != new_move:
            return True
        
        return False

    # move until entity hits a wall
    def find_target_pos(self, x:int, y:int, direction:int) -> tuple[int, int]:
        dx, dy = self.dir_dict[direction]
        target_x, target_y = x, y
        while (target_x+dx, target_y+dy) in self.map.tiles:
            if self.map.tiles[(target_x+dx, target_y+dy)].tangible:
                break # if entity hits a wall
            
            target_x += dx
            target_y += dy

        return target_x, target_y
    
    def update_movement(self) -> None:
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
        if self.moving:
            self.update_movement()
            return
        
        if len(self.move_queue) == 0:
            return
        
        self.initiate_move(self.move_queue[0], delta_time)