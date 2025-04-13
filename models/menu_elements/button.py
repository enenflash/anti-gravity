import pygame as pg
from models.menu_elements.element import *

class Button(Element):
    """Represents a clickable button."""
    def __init__ (self, pixel_pos:tuple[int, int], button_function:str, static_image:pg.Surface, selected_image:pg.Surface, scale:int|float=1) -> None:
        self.function = button_function
        # static image - default image, selected image - when mouse is over
        self.static_image = pg.transform.scale(static_image, (static_image.get_width()*scale, static_image.get_height()*scale))
        self.selected_image = pg.transform.scale(selected_image, (selected_image.get_width()*scale, selected_image.get_height()*scale))
        self.selected = False
        self.pressed = False

        super().__init__(pixel_pos, static_image, scale)

        self.set_button_domains()

    # button domains are used to check if the mouse is on the button
    def set_button_domains(self) -> None:
        self.static_domain = self.pixel_pos[0]-self.static_image.get_width()/2, self.pixel_pos[0]+self.static_image.get_width()/2
        self.static_range = self.pixel_pos[1]-self.static_image.get_height()/2, self.pixel_pos[1]+self.static_image.get_height()/2
        self.selected_domain = self.pixel_pos[0]-self.selected_image.get_width()/2, self.pixel_pos[0]+self.selected_image.get_width()/2
        self.selected_range = self.pixel_pos[1]-self.selected_image.get_height()/2, self.pixel_pos[1]+self.selected_image.get_height()/2

    def set_pixel_pos(self, pixel_x:int|float|None=None, pixel_y:int|float|None=None) -> None:
        if pixel_x != None:
            self.pixel_pos[0] = pixel_x
        if pixel_y != None:
            self.pixel_pos[1] = pixel_y

        self.set_button_domains()

    def check_mouse_over(self, mouse_pos:tuple[int, int]) -> bool:
        # two separate cases for if the button is selected or not in case selected and static images are differently sized
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
    
    def select(self, select:bool) -> None:
        self.selected = select

    def update(self, mouse_pos:tuple[int, int], mouse_pressed:tuple[bool, bool, bool]) -> None:
        self.selected = self.check_mouse_over(mouse_pos)
        self.pressed = self.selected and mouse_pressed[0]
        # menu class will check if button is pressed

    def draw(self, surface:pg.Surface) -> None:
        self.image = self.selected_image if self.selected else self.static_image
        super().draw(surface)

class LevelButton(Button):
    """
    Specifically for drawing the level buttons in the level menu.
    \nHas additional attribute 'level_index' to check what level the button corresponds to.
    """
    def __init__ (self, pixel_pos:tuple[int, int], static_image:pg.Surface, selected_image:pg.Surface, level_index:int, scale:int|float=1) -> None:
        super().__init__ (pixel_pos, "open_map", static_image, selected_image, scale=scale)
        self.level_index = level_index