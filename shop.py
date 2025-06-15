import pygame
import functions as fce
import config as conf
from items import iron_axe,heal_potion,iron_fishing_rod,cisco_certificate

#komentare tady dodelam nekdy

pixel_font = pygame.font.Font(fce.get_path("res/font/Minecraftia-Regular.ttf"), 34) #font, velikost fontu

shop_inventory = []
shop_inventory.append(iron_axe.Iron_axe(conf.TILE_SIZE*0, conf.TILE_SIZE*0,pygame.Vector2(5,5)))
shop_inventory.append(heal_potion.Heal_otion(conf.TILE_SIZE*0, conf.TILE_SIZE*0,pygame.Vector2(5,5)))
shop_inventory.append(iron_fishing_rod.Iron_fishing_rod(conf.TILE_SIZE*0, conf.TILE_SIZE*0,pygame.Vector2(5,5)))
shop_inventory.append(cisco_certificate.Cisco_certificate(conf.TILE_SIZE*0, conf.TILE_SIZE*0,pygame.Vector2(5,5)))

shop_all_background = pygame.Rect(conf.TILE_SIZE*2,conf.TILE_SIZE*9,conf.TILE_SIZE*5,conf.TILE_SIZE*1)
shop_background = pygame.Rect(conf.TILE_SIZE*2,conf.TILE_SIZE*10,conf.TILE_SIZE*15,conf.TILE_SIZE*1)
shop_desc_background = pygame.Rect(conf.TILE_SIZE*2,conf.TILE_SIZE*11,conf.TILE_SIZE*5,conf.TILE_SIZE*1)
shop_cursor = pygame.Rect(conf.TILE_SIZE*(conf.inv_pos+2),conf.TILE_SIZE*10,conf.TILE_SIZE*1,conf.TILE_SIZE*1)

def buy_item(event):
    """E/F hrac muze koupit item z obchodu."""
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_e or event.key == pygame.K_f:
            try:
                if shop_inventory[int((shop_cursor.x/conf.TILE_SIZE)-2)].price <= conf.coins and len(conf.inventory) <= 16:
                    conf.inventory.append(shop_inventory[int((shop_cursor.x/conf.TILE_SIZE)-2)])
                    conf.coins -= shop_inventory[int((shop_cursor.x/conf.TILE_SIZE)-2)].price
                    #del shop_inventory[int((shop_cursor.x/conf.TILE_SIZE)-2)]
            except:
                pass

def manager(event):
    """Pohyb kurzoru v obchode."""
    if conf.shop_pos-event.y >= 0 and conf.shop_pos-event.y <= 14:
        conf.shop_pos-= event.y
        shop_cursor.x-= event.y*conf.TILE_SIZE

def draw(window):
    """Vykresli obchod."""
    pygame.draw.rect(window,"black",shop_all_background,0,10)
    pygame.draw.rect(window,"white",shop_all_background,3,10)

    pygame.draw.rect(window,"black",shop_background,0,10)
    pygame.draw.rect(window,"white",shop_background,3,10)

    pygame.draw.rect(window,"black",shop_desc_background,0,10)
    pygame.draw.rect(window,"white",shop_desc_background,3,10)

    pygame.draw.rect(window,"white",shop_cursor,3,10)

    shop_text = pixel_font.render("SHOP",1,"white")
    window.blit(shop_text,((conf.TILE_SIZE*2)+10,conf.TILE_SIZE*9))

    try:
        price_text = pixel_font.render(f"PRICE: {shop_inventory[int((shop_cursor.x/conf.TILE_SIZE)-2)].price}",1,"white")
        window.blit(price_text,((conf.TILE_SIZE*2)+10,conf.TILE_SIZE*11))
    except:
        price_text = pixel_font.render(f"PRICE:",1,"white")
        window.blit(price_text,((conf.TILE_SIZE*2)+10,conf.TILE_SIZE*11))

    for i in range(19):
        try:
            window.blit(shop_inventory[i].img, (conf.TILE_SIZE*(i+2),conf.TILE_SIZE*10))
        except:
            continue

def close_shop(event):
    """Zavre okno s obchodem."""
    if event.type == pygame.KEYDOWN: #kdyz hrac zmackne escape tak zavre shop
        if event.key == pygame.K_ESCAPE:
            conf.gamemode = conf.GAMEMODE_GAME

def shop_delay_manager():
    """Resi delay pro otevreni shopu. asi."""
    if conf.shop_delay > 0:
        conf.shop_delay = conf.shop_delay -1