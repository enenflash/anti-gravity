from src.settings import *
from src.file_loader import *
from src.background import *
from src.sound import *
from models.menu_elements import *

class Menu:
    def __init__ (self, game:object, screen:pg.Surface, menu_path:str, bg_offset:list[int|float, int|float]=[0, 0], menu_vars:dict={}) -> None:
        self.game = game
        self.input_handler = game.input_handler
        self.screen = screen
        self.surface = pg.Surface((SCREEN_W, SCREEN_H), pg.SRCALPHA)
        
        self.menu_vars = menu_vars
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
                if element["id"] in self.element_data
            ]

        self.texts = []
        if "text" in self.menu_data:
            for text in self.menu_data["text"]:
                self.texts.append(Text(get_pixel_pos(text["pos"]), text["text"], text["size"]/100*SCREEN_H, text["colour"], text["vars"], menu_vars))

        self.buttons = []
        if "buttons" in self.menu_data:
            for button in self.menu_data["buttons"]:
                if button["id"] not in self.button_data: continue
                pos = button["pos"][0]/100*SCREEN_W, button["pos"][1]/100*SCREEN_H
                button_data = self.button_data[button["id"]]
                self.buttons.append(Button(pos, button["function"], button_data["static-image"], button_data["selected-image"], button["scale"]))
        
        self.bg_colour = self.menu_data["background-colour"] if "background-colour" in self.menu_data else [0, 0, 0, 0]
        self.background = Background(self.screen, self.menu_data["tile-background"]) if "tile-background" in self.menu_data else None
        if self.background != None:
            self.background.offset = bg_offset

        self.blend_image = pg.Surface(((self.screen.get_width()-self.surface.get_width())/2, self.surface.get_height()), pg.SRCALPHA)
        self.blend_image.fill([0, 0, 0, 100])

        self.level_scroller = None
        if "level-scroller" in self.menu_data:
            self.level_scroller = LevelScroller(self, get_pixel_pos(self.menu_data["level-scroller"]["pos"]), get_pixel_pos(self.menu_data["level-scroller"]["size"]))

    def do_button_action(self, button:Button) -> None:
        if button.function == "next_game":
            next_level = self.game.game_state_manager.instance.level_index + 1
            if next_level >= len(self.game.game_state_manager.level_manager.get_all_levels()):
                button.function = "levels"
            else:
                map_path = self.game.game_state_manager.level_manager.get_all_levels()[next_level]["path"]
                self.game.game_state_manager.launch_instance(map_path, next_level)
                self.game.game_state_manager.close_menu()
        if button.function == "levels":
            if game_sound.last_played not in("space-dreams", "ambience"):
                game_sound.fadeout_music()
                game_sound.play_indefinite("ambience")
            self.game.game_state_manager.launch_menu("levels", self.background.offset if self.background != None else [0, 0])
            self.game.game_state_manager.close_instance()
        if button.function == "open_map":
            map_path = self.game.game_state_manager.level_manager.get_all_levels()[button.level_index]["path"]
            self.game.game_state_manager.launch_instance(map_path, button.level_index)
            self.game.game_state_manager.close_menu()
        if button.function == "die_screen":
            self.game.game_state_manager.launch_menu("died", self.background.offset if self.background != None else [0, 0])
        if button.function == "resume":
            self.game.game_state_manager.close_menu()
            self.game.game_state_manager.set_pause_instance(False)
        if button.function == "restart":
            if game_sound.last_played != "ambience":
                game_sound.fadeout_music()
                game_sound.play_indefinite("ambience")
            self.game.game_state_manager.restart_instance()
            self.game.game_state_manager.close_menu()
        if button.function == "title_menu":
            self.game.game_state_manager.close_instance()
            self.game.game_state_manager.launch_menu("title", self.background.offset if self.background != None else [0, 0])
            if game_sound.last_played != "space-dreams":
                game_sound.fadeout_music()
            game_sound.play_music("space-dreams")
        if button.function == "quit":
            self.game.game_state_manager.game_quit()
        if button.function == "move_right" and self.level_scroller != None:
            self.level_scroller.move_right()
        if button.function == "move_left" and self.level_scroller != None:
            self.level_scroller.move_left()

    def update(self) -> None:
        if self.background != None:
            self.background.update()

        for button in self.buttons:
            button.update(self.input_handler.mouse_pos, self.input_handler.mouse_pressed)
            if button.pressed:
                game_sound.play_sound("button")
                self.do_button_action(button)

        selected = any([button.selected for button in self.buttons]) or (self.level_scroller.get_selected() if self.level_scroller != None else False)
        self.mouse.update(selected)
        if self.level_scroller != None:
            self.level_scroller.update(self.input_handler.mouse_pos, self.input_handler.mouse_pressed)

    def draw(self) -> None:
        self.surface.fill(self.bg_colour)
        if self.background != None:
            self.background.draw()

        for text in self.texts:
            text.draw(self.surface)
        for element in self.elements:
            element.draw(self.surface)
        for button in self.buttons:
            button.draw(self.surface)
        
        if self.level_scroller != None:
            self.level_scroller.draw(self.surface)
        
        self.screen.blit(self.surface, ((screen_info.current_w-SCREEN_W)/2, 0))
        self.screen.blit(self.blend_image, (0, 0))
        self.screen.blit(self.blend_image, (self.screen.get_width()-self.blend_image.get_width(), 0))
        self.mouse.draw(self.screen, x_offset=(screen_info.current_w-SCREEN_W)/2)