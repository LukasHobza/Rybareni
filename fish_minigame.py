import pygame, random
import config as conf
import functions as fce
from entities import fish_blue_slime

water_index = 0

background_ = pygame.Rect(conf.TILE_SIZE*11+conf.TILE_SIZE/2,conf.TILE_SIZE*4-conf.TILE_SIZE/2,conf.TILE_SIZE*4-conf.TILE_SIZE/2,conf.TILE_SIZE*9)
background = pygame.Rect (conf.TILE_SIZE*11+conf.TILE_SIZE/2,conf.TILE_SIZE*4-conf.TILE_SIZE/2,conf.TILE_SIZE*4-conf.TILE_SIZE/2,conf.TILE_SIZE*9)

min_y = conf.TILE_SIZE*12
max_y = conf.TILE_SIZE*4

#bar
progress_bar = 20
progress_width = conf.TILE_SIZE/2
progress_heihgt = min_y-max_y

#zeleny obdelnik
paddle_speed = conf.TILE_SIZE/40
paddle_speed_cur = 0
paddle_speed_max = 10

paddle_width = conf.TILE_SIZE/2
paddle_height = conf.TILE_SIZE*2
paddle_pos = pygame.Vector2(conf.TILE_SIZE*14,conf.TILE_SIZE*12 - paddle_height)

#rybicka
fish_speed = conf.TILE_SIZE/40
fish_speed_cur = 0
fish_speed_max = 7

fish_width = conf.TILE_SIZE/2
fish_height = conf.TILE_SIZE/2
fish_pos = pygame.Vector2(conf.TILE_SIZE*14,conf.TILE_SIZE*12 - fish_height)

def reset(difficulty):
    global paddle_speed,paddle_speed_cur,paddle_speed_max,paddle_height,paddle_pos,progress_bar
    progress_bar = 20

    #zeleny obdelnik
    paddle_speed = 1
    paddle_speed_cur = 0
    paddle_speed_max = 5

    paddle_height = conf.TILE_SIZE*2
    paddle_pos = pygame.Vector2(conf.TILE_SIZE*14,conf.TILE_SIZE*12 - paddle_height)

    #ryba
    global fish_speed,fish_speed_cur,fish_speed_max,fish_pos
    fish_pos = pygame.Vector2(conf.TILE_SIZE*14,conf.TILE_SIZE*12 - fish_height)
    fish_speed_cur = 0

    match difficulty:
        case "easy":
            fish_speed = 0.2
            fish_speed_max = 3
        case "medium":
            fish_speed = 0.5
            fish_speed_max = 4
        case "hard":
            fish_speed = 1
            fish_speed_max = 5
        case "nightmare":
            fish_speed = 1.2
            fish_speed_max = 6

def draw(display):
    fce.draw_transparent_rect(display,(145,255,255),background_,128,10)
    pygame.draw.rect(display,"black",background,3,10)
    pygame.draw.rect(display, (150,150,150), [conf.TILE_SIZE*12, conf.TILE_SIZE*4, conf.TILE_SIZE/2, conf.TILE_SIZE*8], 0)
    pygame.draw.rect(display, (150,150,150), [conf.TILE_SIZE*14, conf.TILE_SIZE*4, conf.TILE_SIZE/2, conf.TILE_SIZE*8], 0)

    pygame.draw.rect(display, (20,255,20), [paddle_pos.x, paddle_pos.y, paddle_width, paddle_height], 0)#vykresli zelenyobdelnik
    pygame.draw.rect(display, (20,20,255), [fish_pos.x, fish_pos.y, fish_width, fish_height], 0)#vykresli rybicku
    pygame.draw.rect(display, (255-progress_bar,progress_bar,0), [conf.TILE_SIZE*12,conf.TILE_SIZE*12-(progress_heihgt*(progress_bar/255)), progress_width, (progress_heihgt*(progress_bar/255))], 0)#vykresli progress bar

def manager(player, entities):
    #zeleny obdelnik
    global paddle_speed_cur, fish_speed_cur,progress_bar
    keys = pygame.key.get_pressed()#ziska zmacknute klavesy
    if keys[pygame.K_SPACE]:#kdyz hrac drzi mezernik
        if paddle_speed_cur < paddle_speed_max:#pokud rychlost zel ob neni maximalni
            paddle_speed_cur+= paddle_speed#zvyseni aktualni rychlosti
    else:
        if paddle_speed_cur > -paddle_speed_max:
            paddle_speed_cur -= paddle_speed

    if paddle_speed_cur > 0:#pokud je aktualni rychlost kladna
        if paddle_pos.y > max_y:#pokud aktualni vyska neni maximalni
            paddle_pos.y -= paddle_speed_cur#zel ob se posune nahoru
        else:
            paddle_pos.y = max_y#jinak se jeho vyska nastavi na max
    else:
        if paddle_pos.y+paddle_height < min_y:
            paddle_pos.y -= paddle_speed_cur
        else:
            paddle_pos.y = min_y-paddle_height

    #rybicka nahodny pohyb
    if fish_pos.y > max_y+((min_y-max_y)/2):#pokud je ryba v dolni polovine "baru", asi stejne je to jedno
        if random.randint(0,100) <= 57:#je vetsi sance ze ryba pujde nahoru
            if fish_speed_cur < fish_speed_max:
                fish_speed_cur += fish_speed
        else:
            if fish_speed_cur > -fish_speed_max:
                fish_speed_cur -= fish_speed
    else:
        if random.randint(0,100) <= 57:
            if fish_speed_cur > -fish_speed_max:
                fish_speed_cur -= fish_speed
        else:
            if fish_speed_cur < fish_speed_max:
                fish_speed_cur += fish_speed

    #kontrola aby ryba nesla za hranice
    if fish_speed_cur > 0:
        if fish_pos.y > max_y:
            fish_pos.y -= fish_speed_cur
        else:
            fish_pos.y = max_y
    else:
        if fish_pos.y+fish_height < min_y:
            fish_pos.y -= fish_speed_cur
        else:
            fish_pos.y = min_y-fish_height


    zeleny_obdelnik = pygame.Rect(paddle_pos.x, paddle_pos.y, paddle_width, paddle_height)
    rybicka = pygame.Rect(fish_pos.x, fish_pos.y, fish_width, fish_height)
    if zeleny_obdelnik.colliderect(rybicka) and progress_bar+0.8 <= 255:
        progress_bar+=0.8
    elif progress_bar-1 >= 0:
        progress_bar-=1

    if progress_bar >= 250:#kdyz hrac chytne rybu
        match water_index:
            case 0:
                entities.append(fish_blue_slime.Fish(player.pos.x,player.pos.y,conf.cur_map,1,100,10))
            case 1:
                entities.append(fish_blue_slime.Fish(player.pos.x,player.pos.y,conf.cur_map,3,200,20))

        player.invincible_timer = player.invincible_timer_length
        conf.gamemode = conf.GAMEMODE_GAME
    elif progress_bar <= 2:#kdyz hrac nechytne rybu
        conf.gamemode = conf.GAMEMODE_GAME

    if keys[pygame.K_ESCAPE]:#hrac muze zmackout esc a ukoncit rybareni
        conf.gamemode = conf.GAMEMODE_GAME