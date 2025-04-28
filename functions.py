import pygame,sys,os
import tile_manager as tilem
import config as conf

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
    if not player.attacking: #pokud hrac neutoci
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
        entity.pos.x = conf.TILE_SIZE*(conf.ROWS_COLS-2) #prenastavi se pozice hrace na pravou stranu
        if entity.name == "player": #pokud je to hrac
            conf.cur_map.x -= 1  #zmeni se aktualni mapa
            tilem.map_surface, conf.cur_map_data = tilem.change_map() #vygeneruje se nova mapa(velky obrazek), a ziskaji se nova map data
        else:
            entity.map.x -= 1
    elif entity.pos.x >= conf.TILE_SIZE*(conf.ROWS_COLS-2)+conf.TILE_SIZE/2:
        entity.pos.x = conf.TILE_SIZE
        if entity.name == "player":
            conf.cur_map.x += 1
            tilem.map_surface, conf.cur_map_data = tilem.change_map()
        else:
            entity.map.x += 1
    if entity.pos.y <= conf.TILE_SIZE/2:
        entity.pos.y = conf.TILE_SIZE*(conf.ROWS_COLS-2)
        if entity.name == "player":
            conf.cur_map.y -= 1
            tilem.map_surface, conf.cur_map_data = tilem.change_map()
        else:
            entity.map.y -= 1
    elif entity.pos.y >= conf.TILE_SIZE*(conf.ROWS_COLS-2)+conf.TILE_SIZE/2:
        entity.pos.y = conf.TILE_SIZE
        if entity.name == "player":
            conf.cur_map.y += 1
            tilem.map_surface, conf.cur_map_data = tilem.change_map()
        else:
            entity.map.y += 1


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

                    enemy.hp -= player.cur_weapon.damage
                    if enemy.hp < 0:
                        enemy.hp = 0

                    player.can_hit = False
                if player.invincible_timer == 0:
                    player.invincible_timer = player.invincible_timer_length
                    player.hp-=enemy.damage
                return True  # Kolize mezi hráčem a nepřítelem

    return False  # Žádná kolize

def check_collision(entity_img, entity_pos, map_data):
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

def get_path(filename):
    """Bez toho by nefungoval exe soubor."""
    if getattr(sys, 'frozen', False):
        # Program běží jako EXE
        base_path = sys._MEIPASS
    else:
        # Program běží jako normální Python skript
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, filename)