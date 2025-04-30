import pygame
import config as conf

inv_background = pygame.Rect(conf.TILE_SIZE*0,conf.TILE_SIZE*19,conf.TILE_SIZE*19,conf.TILE_SIZE*1)
inv_cursor = pygame.Rect(conf.TILE_SIZE*(conf.inv_pos+0),conf.TILE_SIZE*19,conf.TILE_SIZE*1,conf.TILE_SIZE*1)

def manager(event):
    """Pohyb kurzoru inventare."""
    if conf.inv_pos-event.y >= 0 and conf.inv_pos-event.y <= 18: #kurzor invi nemuze jit pryc z obrazovky
        conf.inv_pos-= event.y #nastaveni pozice v inventari
        inv_cursor.x-= event.y*conf.TILE_SIZE #realna pozice kurzoru v invu

def draw(window):
    """Vykresli inventar."""
    #vykresleni invu
    pygame.draw.rect(window,"black",inv_background,0)
    pygame.draw.rect(window,"white",inv_background,3)

    pygame.draw.rect(window,"white",inv_cursor,3)#vykresleni kurzoru v invu

    #vykresleni itemu v invu
    for i in range(19):
        try:
            window.blit(conf.inventory[i].img, (conf.TILE_SIZE*(i+0),conf.TILE_SIZE*19)) 
        except:
            continue
        