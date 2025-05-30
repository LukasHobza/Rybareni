import pygame
from items import item as i
import config as conf
import functions as fce

class slime_fish_item(i.Item):
    def __init__(self, x,y, map):
        super().__init__(x, y, map)
        self.name = "Heal potion"
        self.value = 10
    
        self.img = pygame.transform.scale(pygame.image.load(fce.get_path("res/blue_slime/blue_slime1.png")),(conf.TILE_SIZE, conf.TILE_SIZE))

    def use(self, player):
        """Pri pouziti doplni zivoty hraci."""
        conf.coins += self.value
        return True
