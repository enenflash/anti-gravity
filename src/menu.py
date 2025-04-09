from settings import *
from file_loader import *
from menu_elements.element import *
from menu_elements.button import *

class Mouse:
    def __init__ (self, input_handler:object) -> None:
        self.input_handler = input_handler
        self.image = FileLoader.get_texture("resources/menu/mouse_yellow.png")
        self.shadow = pg.transform.scale(FileLoader.get_texture("resources/menu/mouse_shadow.png"), (TILE_SIZE*1.2, TILE_SIZE*1.2))
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
        
        if self.anim_time == self.anim_delay:
            self.image_index = self.image_index + 1 if self.image_index < len(self.hover_images) - 1 else 0
            self.anim_time = 0
        self.anim_time += 1

    def draw(self, surface:pg.Surface, x_offset:int=0, y_offset:int=0) -> None:
        if self.selected:
            surface.blit(self.hover_images[self.image_index], (self.pos[0]-TILE_SIZE//2+x_offset, self.pos[1]-TILE_SIZE//2+y_offset))
        surface.blit(self.shadow, (self.pos[0]+x_offset, self.pos[1]+y_offset))
        surface.blit(self.image, (self.pos[0]+x_offset, self.pos[1]+y_offset))

class Menu:
    def __init__ (self, game:object, name:str, screen:pg.Surface, menu_path:str) -> None:
        self.game = game
        self.name = name
        self.input_handler = game.input_handler
        self.screen = screen
        self.surface = pg.Surface((SCREEN_W, SCREEN_H), pg.SRCALPHA)

        self.menu_data = MenuLoader.get_menu_data(menu_path)
        self.button_data = MenuLoader.get_button_data()
        self.element_data = MenuLoader.get_element_data()

        self.mouse = Mouse(self.input_handler)

        get_pixel_pos = lambda pos: (pos[0]/100*SCREEN_W, pos[1]/100*SCREEN_H)
        self.elements = []
        if "elements" in self.menu_data:
            self.elements = [
                Element(get_pixel_pos(element["pos"]), self.element_data[element["id"]]["image"], element["scale"])
                for element in self.menu_data["elements"]
            ]

        self.buttons = []
        if "buttons" in self.menu_data:
            for button in self.menu_data["buttons"]:
                pos = button["pos"][0]/100*SCREEN_W, button["pos"][1]/100*SCREEN_H
                button_data = self.button_data[button["id"]]
                self.buttons.append(Button(pos, button["function"], button_data["static-image"], button_data["selected-image"], button["scale"]))

        self.bg_colour = self.menu_data["static-background"] if "static-background" in self.menu_data else [0, 0, 0, 0]
    
    def do_button_action(self, button:Button) -> None:
        if button.function == "play":
            self.game.game_state_manager.launch_instance("maps/test_maps/test_map_4.json")
            self.game.game_state_manager.close_menu()
        if button.function == "resume":
            self.game.game_state_manager.close_menu()
        if button.function == "title_menu":
            self.game.game_state_manager.close_instance()
            self.game.game_state_manager.launch_menu("menus/title_menu.json", "title")
        if button.function == "quit":
            self.game.game_state_manager.game_quit()

    def update(self) -> None:
        for button in self.buttons:
            button.update(self.input_handler.mouse_pos, self.input_handler.mouse_pressed)
            if button.pressed:
                self.do_button_action(button)

        self.mouse.update(any([button.selected for button in self.buttons]))

    def draw(self) -> None:
        self.surface.fill(self.bg_colour)
        for element in self.elements:
            element.draw(self.surface)
        for button in self.buttons:
            button.draw(self.surface)
        
        self.screen.blit(self.surface, ((screen_info.current_w-SCREEN_W)/2, 0))
        self.mouse.draw(self.screen, x_offset=(screen_info.current_w-SCREEN_W)/2)