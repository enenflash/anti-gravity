from settings import *

class Button:
    def __init__(self, menu:object, id:str, text_path:str, height:float, center_pos:tuple):
        self.menu = menu
        self.id = id
        self.text = menu.image_handler.get_texture(text_path, height, "h")
        self.active = False

        self.border = menu.image_handler.btn_border
        self.active_border = menu.image_handler.active_btn_border

        self.border = menu.image_handler.image_scale(self.border, height, "h")
        self.active_border = menu.image_handler.image_scale(self.active_border, height, "h")

        self.text_pos = center_pos[0] - self.text.get_width()/2, center_pos[1] - self.text.get_height()/2
        self.border_pos = center_pos[0] - self.border.get_width()/2, center_pos[1] - self.border.get_height()/2
        self.active_border_pos = center_pos[0] - self.active_border.get_width()/2, center_pos[1] - self.active_border.get_height()/2

        self.x_range = range(int(center_pos[0] - self.border.get_width()/2), int(center_pos[0] + self.border.get_width()/2))
        self.y_range = range(int(center_pos[1] - self.border.get_height()/2), int(center_pos[1] + self.border.get_height()/2))

    def check_pressed(self):
        if not self.menu.mouse.pressed:
            return None
        
        if self.menu.mouse.pos[0] in self.x_range and self.menu.mouse.pos[1] in self.y_range:
            return True
        
        return False

    def update(self):
        if self.check_pressed():
            self.menu.button_selected = self.id

    def draw(self):
        if self.active:
            self.menu.screen.blit(self.active_border, self.active_border_pos)
        else:
            self.menu.screen.blit(self.border, self.border_pos)
        self.menu.screen.blit(self.text, self.text_pos)

class ButtonDiv:
    def __init__(self, menu, ids:list, text_paths:list, total_height:float, center_pos:tuple, spacing:float=20):
        self.menu = menu

        num_buttons = len(text_paths)
        button_height = (total_height-(spacing*(num_buttons-1)))/num_buttons

        y_start = center_pos[1] - total_height/2 + button_height/2
        current_h = y_start

        self.buttons = []
        for i, path in enumerate(text_paths):
            self.buttons.append(Button(menu, ids[i], path, button_height, (center_pos[0], current_h)))
            current_h += button_height+spacing

        self.active_btn_index = 0

    def update(self):
        if pg.K_UP in self.menu.gamehost.keydowns:
            self.active_btn_index -= 1
        elif pg.K_DOWN in self.menu.gamehost.keydowns:
            self.active_btn_index += 1

        if self.active_btn_index == len(self.buttons):
            self.active_btn_index = 0
        elif self.active_btn_index < 0:
            self.active_btn_index = len(self.buttons) - 1

        for btn in self.buttons: 
            btn.active = False

        self.buttons[self.active_btn_index].active = True

        for btn in self.buttons:
            btn.update()

        self.menu.button_selected = self.buttons[self.active_btn_index].id

    def draw(self):
        for btn in self.buttons:
            btn.draw()

class TextBox:
    def __init__(self, menu:object, text_path:str, width:float, center_pos:tuple):
        self.menu = menu
        self.image = menu.image_handler.get_texture(text_path, width, "w")
        self.pos = center_pos[0] - self.image.get_width()/2, center_pos[1] - self.image.get_height()/2

    def update(self):
        pass

    def draw(self):
        self.menu.screen.blit(self.image, self.pos)