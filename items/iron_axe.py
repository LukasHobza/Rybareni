import pygame
from items import item as i
import config as conf
import functions as fce

class Iron_axe(i.Item):
    def __init__(self, x,y, map):
        super().__init__(x, y, map)
        self.name = "Iron axe"
        self.damage = 90
        self.price = 50
    
        self.img = pygame.transform.scale(pygame.image.load(fce.get_path("res/objects/iron_axe.png")),(conf.TILE_SIZE, conf.TILE_SIZE))

        self.img_left1 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/iron_axe/player_iron_axe_left1.png")),(conf.TILE_SIZE*2, conf.TILE_SIZE))
        self.img_left2 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/iron_axe/player_iron_axe_left2.png")),(conf.TILE_SIZE*2, conf.TILE_SIZE))
        self.img_right1 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/iron_axe/player_iron_axe_right1.png")),(conf.TILE_SIZE*2, conf.TILE_SIZE))
        self.img_right2 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/iron_axe/player_iron_axe_right2.png")),(conf.TILE_SIZE*2, conf.TILE_SIZE))
        self.img_up1 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/iron_axe/player_iron_axe_up1.png")),(conf.TILE_SIZE, conf.TILE_SIZE*2))
        self.img_up2 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/iron_axe/player_iron_axe_up2.png")),(conf.TILE_SIZE, conf.TILE_SIZE*2))
        self.img_down1 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/iron_axe/player_iron_axe_down1.png")),(conf.TILE_SIZE, conf.TILE_SIZE*2))
        self.img_down2 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/iron_axe/player_iron_axe_down2.png")),(conf.TILE_SIZE, conf.TILE_SIZE*2))

    def use(self, player): #komenty viz iron_sword.py
        """Nastavi aktualni zbran + nastavi ze hrac utoci."""
        if not player.tool.name == self.name:
            player.tool = self

        if player.mode == player.normal_mode:
            player.mode = player.attack_mode
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