import pygame, random
import functions as fce
import config as conf
import tile_manager as tilem
from entities import entity as e
from items import slime_fish_item
from items import bronze_coin

class Fish(e.Entity):
    def __init__(self, x,y,map,vel=1,health=100, val=10):
        super().__init__(x, y, map,vel, health)
        self.damage = 10
        self.name = "Basic fish"
        self.value = val

        self.img_1 = pygame.transform.scale(pygame.image.load(fce.get_path("res/fish/animation/blue_slime1.png")),(conf.TILE_SIZE, conf.TILE_SIZE))
        self.img_2 = pygame.transform.scale(pygame.image.load(fce.get_path("res/fish/animation/blue_slime2.png")),(conf.TILE_SIZE, conf.TILE_SIZE))

        self.img_cur = self.img_1

    def drop_item(self):
        """Ryba dropne rnd item kdyz umre."""
        conf.items.append(slime_fish_item.slime_fish_item(self.pos.x,self.pos.y,self.map,self.value))