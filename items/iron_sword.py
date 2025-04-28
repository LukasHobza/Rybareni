import pygame
from items import item as i
import config as conf
import functions as fce

class Iron_sword(i.Item):
    def __init__(self, x,y, map):
        super().__init__(x, y, map)
        self.name = "Iron sword"
        self.damage = 30
    
        self.img = pygame.transform.scale(pygame.image.load(fce.get_path("res/objects/iron_sword.png")),(conf.TILE_SIZE, conf.TILE_SIZE))

        self.img_left1 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/iron_sword/player_iron_sword_left1.png")),(conf.TILE_SIZE*2, conf.TILE_SIZE))
        self.img_left2 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/iron_sword/player_iron_sword_left2.png")),(conf.TILE_SIZE*2, conf.TILE_SIZE))
        self.img_right1 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/iron_sword/player_iron_sword_right1.png")),(conf.TILE_SIZE*2, conf.TILE_SIZE))
        self.img_right2 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/iron_sword/player_iron_sword_right2.png")),(conf.TILE_SIZE*2, conf.TILE_SIZE))
        self.img_up1 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/iron_sword/player_iron_sword_up1.png")),(conf.TILE_SIZE, conf.TILE_SIZE*2))
        self.img_up2 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/iron_sword/player_iron_sword_up2.png")),(conf.TILE_SIZE, conf.TILE_SIZE*2))
        self.img_down1 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/iron_sword/player_iron_sword_down1.png")),(conf.TILE_SIZE, conf.TILE_SIZE*2))
        self.img_down2 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/iron_sword/player_iron_sword_down2.png")),(conf.TILE_SIZE, conf.TILE_SIZE*2))

    def use(self, player):
        """Nastavi aktualni zbran + nastavi ze hrac utoci."""
        if not player.cur_weapon.name == self.name:
            player.cur_weapon = self

        if not player.attacking:
            player.attacking = True
            player.can_hit = True
            player.invincible_timer = player.invincible_timer_length/4
            player.sprite_counter = 0

            player.pos_before_attack = player.pos + (0,0)
            if player.direction == "up":
                player.pos.y -= conf.TILE_SIZE
            elif player.direction == "left":
                player.pos.x -= conf.TILE_SIZE   
                player.attack() 
        return False