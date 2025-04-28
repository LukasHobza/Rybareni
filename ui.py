import pygame
import functions as fce
import config as conf
pygame.font.init()

pixel_font = pygame.font.Font(fce.get_path("res/font/Minecraftia-Regular.ttf"), 42)

def draw(window, player_hp, player_max_hp):
    """Vykresli ui."""
    hp_text = pixel_font.render(f"{player_hp}/{player_max_hp}",1,"white")
    window.blit(hp_text,(5,0))
    coin_text = pixel_font.render(f"{conf.coins}",1,"white")
    window.blit(coin_text,(5,conf.TILE_SIZE*1))