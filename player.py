import pygame, os, random
import config as conf
import functions as fce

from items import iron_sword

class Player:
    def __init__(self, x,y, vel=3,hp=100):
        self.name = "player"
        self.pos = pygame.Vector2(x,y)
        self.pos_before_event = pygame.Vector2(x,y)
        self.hp = hp
        self.max_hp = hp
        self.vel_tiles_per_sec = vel
        self.vel_pixels_per_sec = vel * conf.TILE_SIZE
        self.direction = "down"
        
        #nezranitelnost 
        self.invincible_timer = 0 
        self.invincible_timer_length = 60*2

        #pro animace pri pohybu
        self.sprite_counter = 0
        self.sprite_frek = 20

        self.can_hit = False

        #mode
        self.normal_mode = 0
        self.attack_mode = 1
        self.fish_mode = 2
        self.mode = self.normal_mode

        self.tool = iron_sword.Iron_sword(0,0,(5,5)) #aktualni zbran
        
        self.img_cur = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/normal/player_down1.png")),(conf.TILE_SIZE, conf.TILE_SIZE)) #aktualni obrazek

        self.img_left1 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/normal/player_left1.png")),(conf.TILE_SIZE, conf.TILE_SIZE))
        self.img_left2 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/normal/player_left2.png")),(conf.TILE_SIZE, conf.TILE_SIZE))
        self.img_right1 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/normal/player_right1.png")),(conf.TILE_SIZE, conf.TILE_SIZE))
        self.img_right2 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/normal/player_right2.png")),(conf.TILE_SIZE, conf.TILE_SIZE))
        self.img_up1 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/normal/player_up1.png")),(conf.TILE_SIZE, conf.TILE_SIZE))
        self.img_up2 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/normal/player_up2.png")),(conf.TILE_SIZE, conf.TILE_SIZE))
        self.img_down1 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/normal/player_down1.png")),(conf.TILE_SIZE, conf.TILE_SIZE))
        self.img_down2 = pygame.transform.scale(pygame.image.load(fce.get_path("res/player/normal/player_down2.png")),(conf.TILE_SIZE, conf.TILE_SIZE))

    def fishing(self):
        """Rabareni pro hrace."""
        match self.direction:
            case "left":
                if self.sprite_counter <= self.sprite_frek/2: #nastavi jeden nebo druhy obrazek, dela animaci
                    self.img_cur = self.tool.img_left1
                else:
                    self.img_cur = self.tool.img_left2
                
            case "right": 
                if self.sprite_counter <= self.sprite_frek/2:
                    self.img_cur = self.tool.img_right1
                else:
                    self.img_cur = self.tool.img_right2

            case "up": 
                if self.sprite_counter <= self.sprite_frek/2:
                    self.img_cur = self.tool.img_up1
                else:
                    self.img_cur = self.tool.img_up2

            case "down": 
                if self.sprite_counter <= self.sprite_frek/2:
                    self.img_cur = self.tool.img_down1
                else:
                    self.img_cur = self.tool.img_down2

        if random.randint(0,100) <= 1:
            self.sprite_counter = 0
            self.mode = self.normal_mode #hrac uz nerybari
            self.pos = self.pos_before_event #vrati hrace na pozici pred rybarenim, attack lepe prejmenovat na neco jineho napr event

            match self.direction: #nastavi normalni obrazek hrace, uz ne s prutem
                case "left": 
                    self.img_cur = self.img_left1
                    
                case "right": 
                    self.img_cur = self.img_right1

                case "up": 
                    self.img_cur = self.img_up1

                case "down": 
                    self.img_cur = self.img_down1
            conf.gamemode = conf.GAMEMODE_FISH_MINIGAME
        
        if self.sprite_counter < self.sprite_frek:
            self.sprite_counter+=1

    def attack(self):
        """Utoceni pro hrace."""
        match self.direction:
            case "left":
                if self.sprite_counter <= self.sprite_frek/2: #nastavi jeden nebo druhy obrazek, dela animaci
                    self.img_cur = self.tool.img_left1
                else:
                    self.img_cur = self.tool.img_left2
                
            case "right": 
                if self.sprite_counter <= self.sprite_frek/2:
                    self.img_cur = self.tool.img_right1
                else:
                    self.img_cur = self.tool.img_right2

            case "up": 
                if self.sprite_counter <= self.sprite_frek/2:
                    self.img_cur = self.tool.img_up1
                else:
                    self.img_cur = self.tool.img_up2

            case "down": 
                if self.sprite_counter <= self.sprite_frek/2:
                    self.img_cur = self.tool.img_down1
                else:
                    self.img_cur = self.tool.img_down2

        if self.sprite_counter >= self.sprite_frek:
            self.sprite_counter = 0
            self.mode = self.normal_mode #hrac uz neutoci
            self.can_hit = False #hrac nemuze dat hit
            self.pos = self.pos_before_event #vrati hrace na pozici pred utocenim

            match self.direction: #nastavi normalni obrazek hrace, uz ne se zbrani
                case "left": 
                    self.img_cur = self.img_left1
                    
                case "right": 
                    self.img_cur = self.img_right1

                case "up": 
                    self.img_cur = self.img_up1

                case "down": 
                    self.img_cur = self.img_down1
        
        self.sprite_counter+=1

    def set_image(self, direction):
        """Nastaveni obrazku hrace."""
        match direction: #dela animace hrace
            case "left": 
                if self.sprite_counter <= self.sprite_frek/2:
                    self.img_cur = self.img_left1
                else:
                    self.img_cur = self.img_left2
                
            case "right": 
                if self.sprite_counter <= self.sprite_frek/2:
                    self.img_cur = self.img_right1
                else:
                    self.img_cur = self.img_right2

            case "up": 
                if self.sprite_counter <= self.sprite_frek/2:
                    self.img_cur = self.img_up1
                else:
                    self.img_cur = self.img_up2

            case "down": 
                if self.sprite_counter <= self.sprite_frek/2:
                    self.img_cur = self.img_down1
                else:
                    self.img_cur = self.img_down2

        if self.sprite_counter >= self.sprite_frek:
            self.sprite_counter = 0
        

    def draw(self, window):
        """Vykresleni hrace."""
        window.blit(self.img_cur, (self.pos))

    def manager(self,dt):
        """Pohyb hrace + reseni nezranitelnosti + utoceni hrace."""
        keys = pygame.key.get_pressed()
        move = pygame.Vector2(0,0)

        if self.invincible_timer > 0: #odecteni nezranitelnosti
            self.invincible_timer-=1

        if self.mode == self.normal_mode: #pokud hrac neutoci, pohyb hrace
            if keys[pygame.K_a]:
                move += pygame.Vector2(-1,0)
                self.set_image("left")
                self.direction = "left"
            if keys[pygame.K_d]:
                move += pygame.Vector2(1,0)
                self.set_image("right")
                self.direction = "right"
            if keys[pygame.K_w]:
                move += pygame.Vector2(0,-1)
                self.set_image("up")
                self.direction = "up"
            if keys[pygame.K_s]:
                move += pygame.Vector2(0,1)
                self.set_image("down")
                self.direction = "down"
                
            if move != pygame.Vector2(0,0): #pokud se hrac hybe
                self.sprite_counter += 1
                move = move.normalize()
                move *= self.vel_pixels_per_sec * dt

                new_pos = self.pos + move

                if not fce.check_collision(new_pos, conf.cur_map_data): #kontrola jestli je nova pozice pristupna
                    self.pos = new_pos
                else:
                    match fce.alternative_move(self,move,self.vel_pixels_per_sec * dt):
                        case "left":
                            self.pos.x -= self.vel_pixels_per_sec * dt
                        case "right":
                            self.pos.x += self.vel_pixels_per_sec * dt
                        case "up":
                            self.pos.y -= self.vel_pixels_per_sec * dt
                        case "down":
                            self.pos.y += self.vel_pixels_per_sec * dt

        elif self.mode == self.attack_mode: #pokd hrac utoci
            self.attack()
        elif self.mode == self.fish_mode:
            self.fishing()