import pygame
from items import item as i
import config as conf
import functions as fce
import fish_minigame

class Iron_fishing_rod(i.Item):
    def __init__(self, x,y, map):
        super().__init__(x, y, map)
        self.name = "Iron fishing rod"
        self.height = conf.TILE_SIZE*4
        self.price = 20
    
        self.img = pygame.transform.scale(pygame.image.load(fce.get_path("res/objects/basic_fishing_rod.png")),(conf.TILE_SIZE, conf.TILE_SIZE))

        #nejsou obrazky, potreba predelat
        self.img_left1 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/fishing/player_fish_left1.png")),(conf.TILE_SIZE*2, conf.TILE_SIZE))
        self.img_left2 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/fishing/player_fish_left2.png")),(conf.TILE_SIZE*2, conf.TILE_SIZE))
        self.img_right1 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/fishing/player_fish_right1.png")),(conf.TILE_SIZE*2, conf.TILE_SIZE))
        self.img_right2 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/fishing/player_fish_right2.png")),(conf.TILE_SIZE*2, conf.TILE_SIZE))
        self.img_up1 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/fishing/player_fish_up1.png")),(conf.TILE_SIZE, conf.TILE_SIZE*2))
        self.img_up2 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/fishing/player_fish_up2.png")),(conf.TILE_SIZE, conf.TILE_SIZE*2))
        self.img_down1 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/fishing/player_fish_down1.png")),(conf.TILE_SIZE, conf.TILE_SIZE*2))
        self.img_down2 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/fishing/player_fish_down2.png")),(conf.TILE_SIZE, conf.TILE_SIZE*2))

    def use(self, player):
        """Nastavi aktualni prut + nastavi ze hrac rybari."""
        if not player.tool.name == self.name: #nastavi prut pokud uz neni nastaveny
            player.tool = self
        water_index = fce.check_water(player, conf.cur_map_data)
        if player.mode == player.normal_mode and water_index != -1:
            player.mode = player.fish_mode
            player.sprite_counter = 0 #sprite counter reset

            player.pos_before_event = player.pos + (0,0) #ulozi pozici pred utocenim
            #aby hrac nedashoval
            fish_minigame.water_index = water_index
            match water_index:
                case 0:
                    fish_minigame.reset("easy",self.height)
                case 1:
                    fish_minigame.reset("hard",self.height)
            if player.direction == "up":
                player.pos.y -= conf.TILE_SIZE
            elif player.direction == "left":
                player.pos.x -= conf.TILE_SIZE   
                player.fishing()
        return False #kdyz vrati false tak se item nemaze z invu