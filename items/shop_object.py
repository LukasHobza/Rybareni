import pygame
from items import item as i
import config as conf
import functions as fce

class Shop(i.Item):
    def __init__(self, x,y, map):
        super().__init__(x, y, map)
        self.name = "Shop"
        self.pick_up = False
    
        self.img = pygame.transform.scale(pygame.image.load(fce.get_path("res/objects/shop.png")),(conf.TILE_SIZE, conf.TILE_SIZE))

    def interact(self):
        """Otevre obchod."""
        if conf.shop_delay <= 0:
            conf.gamemode = conf.GAMEMODE_SHOP
            conf.shop_delay = 180