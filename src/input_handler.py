import pygame as pg
from file_loader import *

default_keybinds = {
    "QUIT": "ESCAPE",
    "RESTART": "r",
    "UP": "UP",
    "LEFT": "LEFT",
    "DOWN": "DOWN",
    "RIGHT": "RIGHT"
}

custom_keybinds = FileLoader.open_json("keybinds.json", "data/keybinds.json")

def get_pg_key(command:str) -> object:
    if command not in custom_keybinds:
        return getattr(pg.locals, "K_" + default_keybinds[command])
    
    try:
        return getattr(pg.locals, "K_" + custom_keybinds[command])
    except AttributeError:
        print(f"Custom keybind for {command} is invalid.")
        print(f"Loaded default key: {default_keybinds[command]}")
        return getattr(pg.locals, "K_" + default_keybinds[command])

class InputHandler:
    def __init__ (self) -> None:
        self.keys = pg.key.get_pressed()

        self.keybinds = {}
        for command in default_keybinds:
            self.keybinds[command] = get_pg_key(command)

        self.keydowns = []

    def __get_keydowns(self, keys:dict) -> list[str]:
        return [command for command in self.keybinds if keys[self.keybinds[command]]]

    def update(self) -> None:
        """
        Call InputHandler.update() every game loop
        """
        self.keys = pg.key.get_pressed()
        self.keydowns = self.__get_keydowns(self.keys)

    def game_status(self) -> str|None:
        if "QUIT" in self.keydowns:
            return "QUIT"
        elif "RESTART" in self.keydowns:
            return "RESTART"

    def get_player_movement(self) -> int:
        if "UP" in self.keydowns:
            return 1
        elif "LEFT" in self.keydowns:
            return 2
        elif "DOWN" in self.keydowns:
            return 3
        elif "RIGHT" in self.keydowns:
            return 4
        
        return 0