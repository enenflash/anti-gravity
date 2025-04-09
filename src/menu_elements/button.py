import pygame as pg

class Button:
    def __init__ (self, pixel_pos:tuple[int, int], static_image:pg.Surface, selected_image:pg.Surface) -> None:
        self.pixel_pos = pixel_pos
        self.static_image = static_image
        self.selected_image = selected_image
        self.selected = False

        self.static_domain = self.pixel_pos[0]-self.static_image.get_width()/2, self.pixel_pos[0]+self.static_image.get_width()/2
        self.static_range = self.pixel_pos[1]-self.static_image.get_height()/2, self.pixel_pos[1]+self.static_image.get_height()/2

        self.selected_domain = self.pixel_pos[0]-self.selected_image.get_width()/2, self.pixel_pos[0]+self.selected_image.get_width()/2
        self.selected_range = self.pixel_pos[1]-self.selected_image.get_height()/2, self.pixel_pos[1]+self.selected_image.get_height()/2

    def check_mouse_over(self, mouse_pos:tuple[int, int]) -> bool:
        if self.selected:
            if mouse_pos[0] > self.selected_domain[1] or mouse_pos[0] < self.selected_domain[0]:
                return False
            if mouse_pos[1] > self.selected_range[1] or mouse_pos[1] < self.selected_range[0]:
                return False
            return True
        
        if mouse_pos[0] > self.static_domain[1] or mouse_pos[0] < self.static_domain[0]:
            return False
        if mouse_pos[1] > self.static_range[1] or mouse_pos[1] < self.static_range[0]:
            return False
        return True

    def update(self, mouse_pos:tuple[int, int], mouse_pressed:tuple[bool, bool, bool]) -> None:
        self.selected = self.check_mouse_over(mouse_pos)

    def draw(self, surface:pg.Surface) -> None:
        if self.selected:
            pixel_pos_x = self.pixel_pos[0]-self.selected_image.get_width()/2
            pixel_pos_y = self.pixel_pos[1]-self.selected_image.get_height()/2
            surface.blit(self.selected_image, (pixel_pos_x, pixel_pos_y))
            return
        pixel_pos_x = self.pixel_pos[0]-self.static_image.get_width()/2
        pixel_pos_y = self.pixel_pos[1]-self.static_image.get_height()/2
        surface.blit(self.static_image, (pixel_pos_x, pixel_pos_y))