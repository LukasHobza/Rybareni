import pygame
from items import item as i
import config as conf
import functions as fce

class slime_fish_item(i.Item):
    def __init__(self, x,y, map,val):
        super().__init__(x, y, map)
        self.name = "Slime fish item"
        self.value = val
    
        self.img = pygame.transform.scale(pygame.image.load(fce.get_path("res/fish/item_image/blue_slime.png")),(conf.TILE_SIZE, conf.TILE_SIZE))

    def use(self, player):
        """Pri pouziti doplni coiny hraci."""
        conf.coins += self.value
        return True
