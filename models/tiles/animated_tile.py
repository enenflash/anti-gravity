from .tile import * 

class AnimatedTile(Tile):
    """Tile with animation"""
    def __init__ (self, tile_id:str, images:list[pg.Surface], properties:dict, rotation:int=0) -> None:
        self.images = images
        self.image_index = 0
        self.anim_delay = 4
        self.anim_time = 0
        super().__init__(tile_id, images[0], properties, rotation)

    def update(self) -> None:
        # update image index according to a set delay between frames
        if self.anim_time == self.anim_delay:
            self.image_index = self.image_index + 1 if self.image_index < len(self.images) - 1 else 0
            self.anim_time = 0
        
        self.anim_time += 1
        # sets current image according to image index
        self.image = self.images[self.image_index]