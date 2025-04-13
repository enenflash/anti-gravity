import pygame as pg

class Element:
    """Base menu element non-abstract class (which is not good programming practise but oh well)"""
    def __init__ (self, pixel_pos:tuple[int, int], image:pg.Surface, scale:int|float=1) -> None:
        self.pixel_pos = [pixel_pos[0], pixel_pos[1]]
        new_size = image.get_width()*scale, image.get_height()*scale
        self.image = pg.transform.scale(image, new_size)

    def set_pixel_pos(self, pixel_x:int|float|None=None, pixel_y:int|float|None=None) -> None:
        if pixel_x != None:
            self.pixel_pos[0] = pixel_x
        if pixel_y != None:
            self.pixel_pos[1] = pixel_y
    
    def draw(self, surface:pg.Surface) -> None:
        pixel_pos_x = self.pixel_pos[0]-self.image.get_width()/2
        pixel_pos_y = self.pixel_pos[1]-self.image.get_height()/2
        surface.blit(self.image, (pixel_pos_x, pixel_pos_y))