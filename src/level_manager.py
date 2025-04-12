from file_loader import *

class LevelManager:
    def __init__ (self) -> None:
        self.levels = FileLoader.open_json("levels.json", "data/fixed/levels.json")["levels"]
        self.player_data = FileLoader.open_json("player_data.json", "data/player-data/player_data.json")

    def file_reload(self) -> None:
        self.player_data = FileLoader.open_json("player_data.json", "data/player-data/player_data.json")

    def get_current_level_index(self) -> int:
        return self.player_data["level-index"]

    def get_current_level(self) -> dict:
        """
        Returns level data for current level
        """
        level_index = self.player_data["level-index"]
        if level_index >= len(self.levels):
            level_index = len(self.levels) - 1
        return self.levels[level_index]

    def get_all_levels(self) -> list:
        """
        Returns a list of all level data
        """
        return self.levels
    
    def update_level(self, current_level_index:int) -> None:
        """
        Store current level the player is up to
        """
        # if playing an old level
        # note self.player_data["level-index"] refers to the level the player is allowed to attempt
        if self.player_data["level-index"] > current_level_index + 1:
            return
        self.player_data["level-index"] = min(current_level_index+1, len(self.levels))
        FileLoader.write_json("data/player-data/player_data.json", self.player_data)