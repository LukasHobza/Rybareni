import pygame
from items import item as i
import config as conf
import functions as fce

class Cisco_certificate(i.Item):
    def __init__(self, x,y, map):
        super().__init__(x, y, map)
        self.name = "Cisco certificate"
        self.price = 150
    
        self.img = pygame.transform.scale(pygame.image.load(fce.get_path("res/objects/cisco.png")),(conf.TILE_SIZE, conf.TILE_SIZE))

    def use(self, player):
        """Pri pouziti doplni zivoty hraci."""
        conf.coins += 1
        return False