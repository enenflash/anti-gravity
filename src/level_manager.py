from src.file_loader import *

class LevelManager:
    """
    Manages player level data from json files
    \nUpdates player high scores and the current level index
    """
    def __init__ (self) -> None:
        self.levels = FileLoader.open_json("levels.json", "data/fixed/levels.json")["levels"]
        self.player_data = FileLoader.open_json("player_data.json", "data/player-data/player_data.json")
    
    def file_reload(self) -> None:
        """
        Reload file to update external changes
        """
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
        FileLoader.write_json(PLAYER_DATA_PATH, self.player_data)
    
    def update_high_score(self, index:int, high_score:int|float) -> None:
        """
        Update player high score for a particular level
        """
        if index >= len(self.player_data["high-scores"]):
            for _ in range(len(self.player_data["high-scores"]), index+1):
                self.player_data["high-scores"].append(-1)
        if high_score > self.player_data["high-scores"][index]:
            self.player_data["high-scores"][index] = high_score
        FileLoader.write_json(PLAYER_DATA_PATH, self.player_data)