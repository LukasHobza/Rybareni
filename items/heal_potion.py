import pygame
from items import item as i
import config as conf
import functions as fce

class Heal_otion(i.Item):
    def __init__(self, x,y, map):
        super().__init__(x, y, map)
        self.name = "Heal potion"
    
        self.img = pygame.transform.scale(pygame.image.load(fce.get_path("res/objects/heal_potion.png")),(conf.TILE_SIZE, conf.TILE_SIZE))

    def use(self, player):
        """Pri pouziti doplni zivoty hraci."""
        if player.hp +10 <= player.max_hp:
            player.hp += 10
            return True
        else:
            return False