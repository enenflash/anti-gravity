import pygame as pg

class Element:
    def __init__ (self, pixel_pos:tuple[int, int], image:pg.Surface, scale:int|float=1) -> None:
        self.pixel_pos = pixel_pos
        new_size = image.get_width()*scale, image.get_height()*scale
        self.image = pg.transform.scale(image, new_size)

    def draw(self, surface:pg.Surface) -> None:
        pixel_pos_x = self.pixel_pos[0]-self.image.get_width()/2
        pixel_pos_y = self.pixel_pos[1]-self.image.get_height()/2
        surface.blit(self.image, (pixel_pos_x, pixel_pos_y))