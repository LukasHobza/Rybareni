from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
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

        self.path_update_interval = 30  # počet frame mezi update
        self.path_update_counter = 0
        self.path = []

    def draw(self, window):
        """Vykresli danou entitu."""
        window.blit(self.img_cur, (self.pos))
    
    def set_image(self):
        """Nastavi obrazek pro entity."""
        if self.sprite_counter <= self.sprite_frek/2:
            self.img_cur = self.img_1
        else:
            self.img_cur = self.img_2

        if self.sprite_counter >= self.sprite_frek:
            self.sprite_counter = 0

    def update_path(self, player_pos):
        """Aktualizuje cestu k hráči."""
        grid = fce.create_grid(conf.cur_map_data)  # Vytvoříme grid z mapy
        start = grid.node(int((self.pos.x+conf.TILE_SIZE/2) // conf.TILE_SIZE), int((self.pos.y+conf.TILE_SIZE/2) // conf.TILE_SIZE))
        end = grid.node(int((player_pos.x+conf.TILE_SIZE/2) // conf.TILE_SIZE), int((player_pos.y+conf.TILE_SIZE/2) // conf.TILE_SIZE))
        
        finder = AStarFinder()
        self.path, _ = finder.find_path(start, end, grid)
        grid.cleanup()  # Uvolníme paměť

    def move(self,player):
        """Pohyb entity podle cesty."""
        self.path_update_counter += 1
        if self.path_update_counter >= self.path_update_interval or not self.path:
            self.update_path(player.pos)
            self.path_update_counter = 0
        if len(self.path) > 1:
            self.sprite_counter+=1
            self.set_image()
            target = self.path[1]
            target_pos = pygame.Vector2(target.x * conf.TILE_SIZE, target.y * conf.TILE_SIZE)

            #Pokud jsme dostatečně blízko, přejdi na další bod v cestě
            if self.pos.distance_to(target_pos) < 2:
                self.pos = target_pos
                self.path.pop(1)
            else:
                move = (target_pos - self.pos).normalize() * self.vel
                self.pos += move

    def draw_hp_bar(self, window):
        """Pokud je potreba vykresli hp bar."""
        if self.hp_bar_dur_cur > 0:
            self.hp_bar_dur_cur-=1
            pygame.draw.rect(window, "red", (self.pos.x, self.pos.y + conf.TILE_SIZE+2, conf.TILE_SIZE,10))
            pygame.draw.rect(window, "green", (self.pos.x, self.pos.y + conf.TILE_SIZE+2, conf.TILE_SIZE * (self.hp/self.max_hp),10))

    def draw_debug_path(self, surface):
        for node in self.path:
            pygame.draw.rect(surface, (0, 255, 0), 
                pygame.Rect(node.x * conf.TILE_SIZE, node.y * conf.TILE_SIZE, conf.TILE_SIZE, conf.TILE_SIZE), 1)
