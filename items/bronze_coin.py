import pygame
from items import item as i
import config as conf
import functions as fce

class Bronze_coin(i.Item):
    def __init__(self, x,y, map):
        super().__init__(x, y, map)
        self.name = "Bronze coin"
    
        self.img = pygame.transform.scale(pygame.image.load(fce.get_path("res/objects/bronze_coin.png")),(conf.TILE_SIZE, conf.TILE_SIZE))

    def use(self, player):
        """Pri pouziti prida jeden coin."""
        conf.coins += 1
        return True