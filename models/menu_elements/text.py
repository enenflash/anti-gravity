from .element import *
from src.settings import *

import pygame as pg
pg.font.init()

class Text(Element):
    """Simple text element which draws based on text rather than image"""
    def __init__ (self, pixel_pos:tuple[int, int], text:str, size:int|float, colour:str|list, text_vars:dict, menu_vars:dict) -> None:
        custom_font = pg.font.Font(CUSTOM_FONT, int(size))
        self.text_str = text
        for var in text_vars:
            if text_vars[var] not in menu_vars:
                continue
            self.text_str = self.text_str.replace(var, str(menu_vars[text_vars[var]]))
        self.text = custom_font.render(self.text_str, False, colour)
        super().__init__(pixel_pos, self.text, 1)