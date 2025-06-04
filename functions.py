from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import pygame,sys,os
import tile_manager as tilem
import config as conf
from items import basic_fishing_rod, iron_sword

def drop_item(event,player):
    """Kdyz je zmacknute Q hrac vyhodi item."""
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_q:
            try: #kdyz v invu neni zadny item tak ta hra nespadne
                item = conf.inventory[conf.inv_pos] #ziskani itemu
                item.pos = player.pos #item ziska pozici hrace
                item.map = conf.cur_map+(0,0) #item se dropne na stejnou pamu na ktere je hrac
                item.dropped_item_delay = 60*2 #delay aby hrac dropnuty item hned nesebral
                conf.items.append(item) #pridani itemu na mapu
                del conf.inventory[conf.inv_pos] #odebrani itemu z invu
            except:
                pass

def show_cords(player):
    """Vypise x,y hrace prepocitane na tile."""
    print(f"X: {round(player.pos.x/conf.TILE_SIZE)}, Y: {round(player.pos.y/conf.TILE_SIZE)}")

def use_item(event, player):
    """Kdyz je zmacknute E/F hrac pouzije item."""
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_e or event.key == pygame.K_f:
            try:
                if conf.inventory[conf.inv_pos].use(player): #pokud je mozne item pouzit
                    del conf.inventory[conf.inv_pos] #odebrani itemu z invu
                    conf.use_delay = 30 #delay na pouziti itemu
            except:
                pass

def pick_up_check(player):
    """Kontrola jesli hrac sebere item."""
    if player.mode == player.normal_mode: #pokud hrac neutoci
        player_mask = pygame.mask.from_surface(player.img_cur)

        for item in conf.items[:]:
            if item.map == conf.cur_map:
                item_mask = pygame.mask.from_surface(item.img)

                offset = (item.pos.x - player.pos.x, item.pos.y - player.pos.y)
                if player_mask.overlap(item_mask, offset): #kdyz se hrac a item prekryvaji
                    if len(conf.inventory) <= 16 and item.dropped_item_delay == 0 and item.pick_up: #pokud je misto v invu, item muze byt sebran
                        conf.inventory.append(item)
                        conf.items.remove(item)
                        del item
                    elif not item.pick_up: #pokud item nemuze byt sebran
                        item.interact() #item zustava na mape a vola se nejaka fce
                    return True
    return False

def map_escape_check(entity):
    """Kontrola jestli entita odesla z mapy."""
    if entity.pos.x <= conf.TILE_SIZE/2: #pokud hrac odesel vlevo z mapy
        if entity.name == "player": #pokud je to hrac
            if entity.mode == entity.normal_mode:
                conf.cur_map.x -= 1  #zmeni se aktualni mapa
                entity.pos.x = conf.TILE_SIZE*(conf.COLS-2) #prenastavi se pozice hrace na pravou stranu
                tilem.map_surface, conf.cur_map_data = tilem.change_map() #vygeneruje se nova mapa(velky obrazek), a ziskaji se nova map data
        else:
            entity.map.x -= 1
            entity.pos.x = conf.TILE_SIZE*(conf.COLS-2) #prenastavi se pozice entity na pravou stranu
    elif entity.pos.x >= conf.TILE_SIZE*(conf.COLS-2)+conf.TILE_SIZE/2:
        if entity.name == "player":
            if entity.mode == entity.normal_mode:
                conf.cur_map.x += 1
                entity.pos.x = conf.TILE_SIZE
                tilem.map_surface, conf.cur_map_data = tilem.change_map()
        else:
            entity.map.x += 1
            entity.pos.x = conf.TILE_SIZE
    if entity.pos.y <= conf.TILE_SIZE/2:
        if entity.name == "player":
            if entity.mode == entity.normal_mode:
                conf.cur_map.y -= 1
                entity.pos.y = conf.TILE_SIZE*(conf.ROWS-2)
                tilem.map_surface, conf.cur_map_data = tilem.change_map()
        else:
            entity.map.y -= 1
            entity.pos.y = conf.TILE_SIZE*(conf.ROWS-2)
    elif entity.pos.y >= conf.TILE_SIZE*(conf.ROWS-2)+conf.TILE_SIZE/2:
        if entity.name == "player":
            if entity.mode == entity.normal_mode:
                conf.cur_map.y += 1
                entity.pos.y = conf.TILE_SIZE
                tilem.map_surface, conf.cur_map_data = tilem.change_map()
        else:
            entity.map.y += 1
            entity.pos.y = conf.TILE_SIZE


def check_hit(player, entities):
    """Kontrola hitu playerXenemak / enemakXplayer."""
    player_mask = pygame.mask.from_surface(player.img_cur)

    for enemy in entities:
        if enemy.map == conf.cur_map:
            enemy_mask = pygame.mask.from_surface(enemy.img_cur)

            offset = (enemy.pos.x - player.pos.x, enemy.pos.y - player.pos.y)
            if player_mask.overlap(enemy_mask, offset):
                if player.can_hit:
                    enemy.hp_bar_dur_cur = enemy.hp_bar_dur #bude se zobrazovat hp bar

                    enemy.hp -= player.tool.damage
                    if enemy.hp < 0:
                        enemy.hp = 0

                    player.can_hit = False
                if player.invincible_timer == 0:
                    player.invincible_timer = player.invincible_timer_length
                    player.hp-=enemy.damage
                return True  # Kolize mezi hráčem a nepřítelem

    return False  # Žádná kolize

def check_collision(entity_pos, map_data):
    """Kontrola kolize."""
    #entity_mask = pygame.mask.from_surface(entity_img)
    tile_size = conf.TILE_SIZE  
    entity_rect = pygame.Rect(entity_pos.x +10, entity_pos.y +10, tile_size -20, tile_size -20)
    
    # Přepočet souřadnic entity na indexy v mapě
    start_col = max(0, int(entity_pos.x // tile_size) - 1)
    end_col = min(len(map_data[0]), int(entity_pos.x // tile_size) + 2)
    start_row = max(0, int(entity_pos.y // tile_size) - 1)
    end_row = min(len(map_data), int(entity_pos.y // tile_size) + 2)

    for row_idx in range(start_row, end_row):
        for col_idx in range(start_col, end_col):
            tile_id = map_data[row_idx][col_idx]
            tile = tilem.tiles[tile_id]

            if tile.collision:  # Kontrolujeme jen blokující dlaždice
                tile_rect = pygame.Rect(col_idx * tile_size, row_idx * tile_size, tile_size, tile_size)
                #tile_mask = tile.mask  # Použijeme předvytvořenou masku
                
                #offset = (tile_rect.x - int(entity_pos.x), tile_rect.y - int(entity_pos.y))

                #if entity_mask.overlap(tile_mask, offset):
                    #return True  
                if entity_rect.colliderect(tile_rect):
                    return True
                
    return False  

def alternative_move(entity, move, vel):
    if move.x < 0:
        if not check_collision(pygame.Vector2(entity.pos.x-vel,entity.pos.y),conf.cur_map_data):
            return "left"
    if move.x > 0:
        if not check_collision(pygame.Vector2(entity.pos.x+vel,entity.pos.y),conf.cur_map_data):
            return "right"
    if move.y < 0:
        if not check_collision(pygame.Vector2(entity.pos.x,entity.pos.y-vel),conf.cur_map_data):
            return "up"
    if move.y > 0:
        if not check_collision(pygame.Vector2(entity.pos.x,entity.pos.y+vel),conf.cur_map_data):
            return "down"
    return "none"

def check_water(player, map_data):
    """Kontrola kolize."""
    tile_size = conf.TILE_SIZE

    new_player_pos = player.pos + pygame.Vector2(0,0)
    match player.direction:
        case "left":
            new_player_pos.x -= conf.TILE_SIZE
                
        case "right": 
            new_player_pos.x += conf.TILE_SIZE

        case "up": 
            new_player_pos.y -= conf.TILE_SIZE

        case "down": 
            new_player_pos.y += conf.TILE_SIZE

    entity_rect = pygame.Rect(new_player_pos.x +10, new_player_pos.y +10, tile_size -20, tile_size -20)
    try:
        # Přepočet souřadnic entity na indexy v mapě
        start_col = max(0, int(new_player_pos.x // tile_size) - 1)
        end_col = min(len(map_data[0]), int(new_player_pos.x // tile_size) + 2)
        start_row = max(0, int(new_player_pos.y // tile_size) - 1)
        end_row = min(len(map_data), int(new_player_pos.y // tile_size) + 2)

        for row_idx in range(start_row, end_row):
            for col_idx in range(start_col, end_col):
                tile_id = map_data[row_idx][col_idx]
                tile = tilem.tiles[tile_id]

                tile_rect = pygame.Rect(col_idx * tile_size, row_idx * tile_size, tile_size, tile_size)
                if entity_rect.colliderect(tile_rect):
                    return tile.water
                    
    except:
        return 0

def get_path(filename): #od chat gpt
    """Funkce na cestu k souboru, důležité pro EXE i normální běh."""
    if getattr(sys, 'frozen', False):
        # Program běží jako EXE
        base_path = sys._MEIPASS
    else:
        # Program běží jako normální Python skript
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path, filename)

def create_grid(map_data): #od chat gpt
    """Vytvoří grid pro pathfinding."""
    grid = Grid(matrix=[[0 if tile <= conf.last_solid else 1 for tile in row] for row in map_data])
    return grid

def debug(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_F1:
            if conf.debug:
                conf.debug = False
            else:
                conf.debug = True

def draw_transparent_rect(target_surface, color, rect, alpha, border_radius=0): #od chat gpt
    """
    Vykreslí průhledný (i zaoblený) obdélník na cílový surface.

    :param target_surface: Surface, na který se má kreslit (např. screen)
    :param color: RGB barva (např. (255, 0, 0))
    :param rect: pygame.Rect nebo (x, y, šířka, výška)
    :param alpha: Průhlednost (0–255)
    :param border_radius: Poloměr zaoblení rohů (0 = bez zaoblení)
    """
    s = pygame.Surface((rect[2], rect[3]), pygame.SRCALPHA)
    pygame.draw.rect(s, (*color, alpha), (0, 0, rect[2], rect[3]), border_radius=border_radius)
    target_surface.blit(s, (rect[0], rect[1]))

def reset(player):
    conf.inventory = []
    conf.inventory.append(basic_fishing_rod.Basic_fishing_rod(0,0,0))
    conf.inventory.append(iron_sword.Iron_sword(0,0,0))

    conf.entities = []

    player.pos = pygame.Vector2(conf.TILE_SIZE*9,conf.TILE_SIZE*9)
    player.level = 1
    player.hp = player.max_hp

    conf.coins = 6

    conf.cur_map = pygame.Vector2(5,5)