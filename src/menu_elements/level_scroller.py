import math, pygame as pg
from file_loader import *
from menu_elements.element import *
from menu_elements.button import *

class LevelScroller(Element):
    def __init__ (self, menu:object, pixel_pos:tuple[int, int], size:tuple[int, int]) -> None:
        self.menu = menu
        self.size = size
        self.image = pg.Surface(size, pg.SRCALPHA)
        self.spacing = 0.05*SCREEN_W

        player_data = FileLoader.open_json("player_data.json", "data/player-data/player_data.json")
        current_level = player_data["level-index"]

        level_buttons = FileLoader.open_json("level_buttons.json", "data/level_buttons.json")
        num_buttons = len(FileLoader.open_json("levels.json", "data/fixed/levels.json")["levels"])

        current_level = min(num_buttons-1, current_level)

        self.offset = 0

        if MENU_SIZE*(current_level+1)+self.spacing*current_level <= self.size[0]:
            self.max_offset = 0
        else:
            self.max_offset = MENU_SIZE*(current_level+1)+self.spacing*current_level - self.size[0]

        self.offset = self.max_offset

        convert_to_str = lambda x: str(x) if len(str(x)) == 2 else "0" + str(x)

        self.buttons = [
            LevelButton(
                (0, self.size[1]/2),
                FileLoader.get_texture(level_buttons[convert_to_str(i)]["static"], MENU_SIZE, MENU_SIZE),
                FileLoader.get_texture(level_buttons[convert_to_str(i)]["selected"], MENU_SIZE, MENU_SIZE),
                level_index=i
            )
            for i in range(current_level+1)
        ]
        super().__init__(pixel_pos, self.image, 1)

        self.blend_image = pg.Surface((MENU_SIZE*2.5, self.size[1]), pg.SRCALPHA)

    def move_right(self) -> None:
        self.offset += MENU_SIZE+0.09*SCREEN_W
        self.offset = min(self.max_offset, self.offset)

    def move_left(self) -> None:
        self.offset -= MENU_SIZE+0.09*SCREEN_W
        self.offset = max(self.offset, -MENU_SIZE/2)

    def get_selected(self) -> bool:
        return any([button.selected for button in self.buttons])

    def button_within_bounds(self, button:LevelButton) -> bool:
        if button.pixel_pos[0]+MENU_SIZE/2 < 0 or button.pixel_pos[0]-MENU_SIZE/2 >= self.size[0]:
            return False
        
        return True
    
    def mouse_within_bounds(self, mouse_pos:tuple[int|float, int|float]):
        if mouse_pos[0] < 0 or mouse_pos[0] >= self.size[0]:
            return False
        
        return True

    def update(self, mouse_pos:tuple[int, int], mouse_pressed:tuple[bool, bool, bool]) -> None:
        # corrected according to level scroller size
        mouse_pos_corrected = (mouse_pos[0]-(self.pixel_pos[0]-self.size[0]/2), mouse_pos[1]-(self.pixel_pos[1]-self.size[1]/2))
        
        if True: #self.max_offset != 0:
            for i, button in enumerate(self.buttons):
                button.set_pixel_pos(pixel_x=MENU_SIZE*i+self.spacing*i-self.offset)

        if not self.mouse_within_bounds(mouse_pos_corrected):
            for button in self.buttons:
                button.select(False)
            return
        
        for button in self.buttons:
            button.update(mouse_pos_corrected, mouse_pressed)
            if button.pressed:
                self.menu.do_button_action(button)

    def draw(self, surface:pg.Surface) -> None:
        # num_buttons = math.ceil((self.size[0] + self.offset) / (MENU_SIZE + self.spacing))
        self.image.fill([0, 0, 0, 0])
        for i, button in enumerate(self.buttons):
            if i != len(self.buttons) - 1:
                pg.draw.line(self.image, "white", (button.pixel_pos[0]+MENU_SIZE/2, button.pixel_pos[1]), (button.pixel_pos[0]+self.spacing+MENU_SIZE/2, button.pixel_pos[1]), 2)
            if not self.button_within_bounds(button):
                continue
            button.draw(self.image)
        
        self.blend_image.fill([0, 0, 0, 150])
        self.image.blit(self.blend_image, (0, 0))
        self.blend_image.fill([0, 0, 0, 100])
        self.image.blit(self.blend_image, (self.blend_image.get_width(), 0))
        self.blend_image.fill([0, 0, 0, 50])
        self.image.blit(self.blend_image, (self.blend_image.get_width()*2, 0))
        super().draw(surface)