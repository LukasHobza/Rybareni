import pygame
from items import item as i
import config as conf
import functions as fce

class Basic_fishing_rod(i.Item):
    def __init__(self, x,y, map):
        super().__init__(x, y, map)
        self.name = "Basic fishing rod"
    
        self.img = pygame.transform.scale(pygame.image.load(fce.get_path("res/objects/basic_fishing_rod.png")),(conf.TILE_SIZE, conf.TILE_SIZE))

        #nejsou obrazky, potreba predelat
        self.img_left1 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/iron_sword/player_iron_sword_left1.png")),(conf.TILE_SIZE*2, conf.TILE_SIZE))
        self.img_left2 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/iron_sword/player_iron_sword_left2.png")),(conf.TILE_SIZE*2, conf.TILE_SIZE))
        self.img_right1 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/iron_sword/player_iron_sword_right1.png")),(conf.TILE_SIZE*2, conf.TILE_SIZE))
        self.img_right2 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/iron_sword/player_iron_sword_right2.png")),(conf.TILE_SIZE*2, conf.TILE_SIZE))
        self.img_up1 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/iron_sword/player_iron_sword_up1.png")),(conf.TILE_SIZE, conf.TILE_SIZE*2))
        self.img_up2 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/iron_sword/player_iron_sword_up2.png")),(conf.TILE_SIZE, conf.TILE_SIZE*2))
        self.img_down1 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/iron_sword/player_iron_sword_down1.png")),(conf.TILE_SIZE, conf.TILE_SIZE*2))
        self.img_down2 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/iron_sword/player_iron_sword_down2.png")),(conf.TILE_SIZE, conf.TILE_SIZE*2))

    def use(self, player):
        """Nastavi aktualni prut + nastavi ze hrac rybari."""
        if not player.tool.name == self.name: #nastavi prut pokud uz neni nastaveny
            player.tool = self

        if player.mode == player.normal_mode:
            #player.mode = player.fish_mode #hrac zacne utocit
            player.sprite_counter = 0 #sprite counter reset

            player.pos_before_attack = player.pos + (0,0) #ulozi pozici pred utocenim
            #aby hrac nedashoval
            """
            if player.direction == "up":
                player.pos.y -= conf.TILE_SIZE
            elif player.direction == "left":
                player.pos.x -= conf.TILE_SIZE   
                player.attack() 
            """
            print("A")
            print(fce.check_water(player,conf.cur_map_data))
        return False #kdyz vrati false tak se item nemaze z invu