import pygame, os, random
import config as conf
import tile_manager as tilem
import functions as fce

class Entity:
    def __init__(self, x,y, map,vel=1,hp=100):
        self.pos = pygame.Vector2(x,y)
        self.map = map
        self.vel = vel
        self.direction = "stop"

        self.hp = hp
        self.max_hp = hp
        self.hp_bar_dur = 60*10
        self.hp_bar_dur_cur = 0

        self.sprite_counter = 0
        self.sprite_frek = 20
        
        self.move_interval = 0
        self.move_frek = 60 * 2

    def draw(self, window):
        """Vykresli danou entitu."""
        window.blit(self.img_cur, (self.pos))

    def move(self, player):
        """Pohyb entity."""
        move = player.pos - self.pos

        """rnd pohyb
        if self.move_interval >= self.move_frek:
            self.move_interval = 0
            self.direction = random.choice(["left", "right", "up", "down", "stop"])
        else:
            self.move_interval+=1


        if self.direction == "left":
            move += pygame.Vector2(-1,0)
            self.set_image()
        if self.direction == "right":
            move += pygame.Vector2(1,0)
            self.set_image()
        if self.direction == "up":
            move += pygame.Vector2(0,-1)
            self.set_image()
        if self.direction == "down":
            move += pygame.Vector2(0,1)
            self.set_image()
        """
        
        if move != pygame.Vector2(0,0): 
            self.sprite_counter += 1
            move = move.normalize()
            move *= self.vel

            new_pos = self.pos + move

            if not fce.check_collision(new_pos, conf.cur_map_data):
                self.pos = new_pos
            else:
                match fce.alternative_move(self,move):
                    case "left":
                        self.pos.x -= self.vel
                    case "right":
                        self.pos.x += self.vel
                    case "up":
                        self.pos.y -= self.vel
                    case "down":
                        self.pos.y += self.vel

    def draw_hp_bar(self, window):
        """Pokud je potreba vykresli hp bar."""
        if self.hp_bar_dur_cur > 0:
            self.hp_bar_dur_cur-=1
            pygame.draw.rect(window, "red", (self.pos.x, self.pos.y + conf.TILE_SIZE+2, conf.TILE_SIZE,10))
            pygame.draw.rect(window, "green", (self.pos.x, self.pos.y + conf.TILE_SIZE+2, conf.TILE_SIZE * (self.hp/self.max_hp),10))
