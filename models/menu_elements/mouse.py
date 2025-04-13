from src.file_loader import *

class Mouse:
    """Class representing the mouse. Used by input handler."""
    def __init__ (self, input_handler:object) -> None:
        self.input_handler = input_handler
        self.image = FileLoader.get_texture("resources/menu/mouse_yellow.png")
        self.shadow = pg.transform.scale(FileLoader.get_texture("resources/menu/mouse_shadow.png"), (TILE_SIZE*1.2, TILE_SIZE*1.2))
        # reuses the blue portal tile animation
        self.hover_images = FileLoader.get_textures("resources/tiles/sprite_sheets/blue_portal.png")
        self.pos = (0, 0)
        self.selected = False
        
        self.image_index = 0
        self.anim_delay = 4
        self.anim_time = 0

    def update(self, selected:bool) -> None:
        self.selected = selected
        self.pos = self.input_handler.mouse_pos

        if not selected:
            return
        
        # updates image index for the hover over button animation
        if self.anim_time == self.anim_delay:
            self.image_index = self.image_index + 1 if self.image_index < len(self.hover_images) - 1 else 0
            self.anim_time = 0
        self.anim_time += 1

    def draw(self, surface:pg.Surface, x_offset:int=0, y_offset:int=0) -> None:
        # draw hover animation if hovering over a button
        if self.selected:
            surface.blit(self.hover_images[self.image_index], (self.pos[0]-TILE_SIZE//2+x_offset, self.pos[1]-TILE_SIZE//2+y_offset))
        surface.blit(self.shadow, (self.pos[0]+x_offset, self.pos[1]+y_offset))
        surface.blit(self.image, (self.pos[0]+x_offset, self.pos[1]+y_offset))