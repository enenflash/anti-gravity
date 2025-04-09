from settings import *
from file_loader import *
from menu_elements.element import *
from menu_elements.button import *

class Menu:
    def __init__ (self, game:object, screen:pg.Surface, menu_path:str) -> None:
        self.game = game
        self.input_handler = game.input_handler
        self.screen = screen
        self.surface = pg.Surface((SCREEN_W, SCREEN_H), pg.SRCALPHA)

        self.menu_data = MenuLoader.get_menu_data(menu_path)
        self.button_data = MenuLoader.get_button_data()
        self.element_data = MenuLoader.get_element_data()

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
    
    def do_button_action(self, button:Button) -> None:
        if button.function == "play":
            self.game.game_state_manager.launch_instance("maps/level1.json")
            self.game.game_state_manager.close_menu()

    def update(self) -> None:
        for button in self.buttons:
            button.update(self.input_handler.mouse_pos, self.input_handler.mouse_pressed)
            if button.pressed:
                self.do_button_action(button)

    def draw(self) -> None:
        self.surface.fill("BLACK")
        for element in self.elements:
            element.draw(self.surface)
        for button in self.buttons:
            button.draw(self.surface)
        self.input_handler.draw_mouse(self.surface)
        self.screen.blit(self.surface, (0, 0))