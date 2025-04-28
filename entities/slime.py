import pygame, random
import config as conf
import tile_manager as tilem
import functions as fce
from entities import entity as e
from items import heal_potion
from items import bronze_coin

class Slime(e.Entity):
    def __init__(self, x,y,map,vel=1,health=100):
        super().__init__(x, y, map,vel, health)
        self.damage = 10
        self.name = "Blue slime"

        self.img_1 = pygame.transform.scale(pygame.image.load(fce.get_path("res/blue_slime/blue_slime1.png")),(conf.TILE_SIZE, conf.TILE_SIZE))
        self.img_2 = pygame.transform.scale(pygame.image.load(fce.get_path("res/blue_slime/blue_slime2.png")),(conf.TILE_SIZE, conf.TILE_SIZE))

        self.img_cur = self.img_1

    def set_image(self):
        """Nastavi obrazek pro slima."""
        if self.sprite_counter <= self.sprite_frek/2:
            self.img_cur = self.img_1
        else:
            self.img_cur = self.img_2

        if self.sprite_counter >= self.sprite_frek:
            self.sprite_counter = 0

    def drop_item(self):
        """Slime dropne rnd item kdyz umre."""
        conf.items.append(random.choice([heal_potion.Heal_otion(self.pos.x,self.pos.y,self.map),bronze_coin.Bronze_coin(self.pos.x,self.pos.y,self.map)]))