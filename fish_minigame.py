import pygame, random
import functions as fce
import config as conf

min_y = conf.TILE_SIZE*12
max_y = conf.TILE_SIZE*4

#bar
progress_bar = 20
progress_width = conf.TILE_SIZE/2
progress_heihgt = min_y-max_y

#zeleny obdelnik
paddle_speed = 1
paddle_speed_cur = 0
paddle_speed_max = 10

paddle_width = conf.TILE_SIZE/2
paddle_height = conf.TILE_SIZE*2
paddle_pos = pygame.Vector2(conf.TILE_SIZE*14,conf.TILE_SIZE*12 - paddle_height)

#rybicka
fish_speed = 1
fish_speed_cur = 0
fish_speed_max = 7

fish_width = conf.TILE_SIZE/2
fish_height = conf.TILE_SIZE/2
fish_pos = pygame.Vector2(conf.TILE_SIZE*14,conf.TILE_SIZE*12 - fish_height)

def reset(difficulty):
    #zeleny obdelnik
    global paddle_speed,paddle_speed_cur,paddle_speed_max,paddle_height,paddle_pos
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
    pygame.draw.rect(display, (20,255,20), [paddle_pos.x, paddle_pos.y, paddle_width, paddle_height], 0)
    pygame.draw.rect(display, (20,20,255), [fish_pos.x, fish_pos.y, fish_width, fish_height], 0)
    pygame.draw.rect(display, (255-progress_bar,progress_bar,0), [conf.TILE_SIZE*12,conf.TILE_SIZE*12-(progress_heihgt*(progress_bar/255)), progress_width, (progress_heihgt*(progress_bar/255))], 0)

def manager():
    #zeleny obdelnik
    global paddle_speed_cur, fish_speed_cur,progress_bar
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if paddle_speed_cur < paddle_speed_max:
            paddle_speed_cur+= paddle_speed
    else:
        if paddle_speed_cur > -paddle_speed_max:
            paddle_speed_cur -= paddle_speed

    if paddle_speed_cur > 0:
        if paddle_pos.y > max_y:
            paddle_pos.y -= paddle_speed_cur
        else:
            paddle_pos.y = max_y
    else:
        if paddle_pos.y+paddle_height < min_y:
            paddle_pos.y -= paddle_speed_cur
        else:
            paddle_pos.y = min_y-paddle_height

    #rybicka nahodny pohyb
    if fish_pos.y > max_y+((min_y-max_y)/2):
        if random.randint(0,100) <= 57:
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
    if zeleny_obdelnik.colliderect(rybicka) and progress_bar+2 <= 255:
        progress_bar+=1
    elif progress_bar > 0:
        progress_bar-=1
    print(progress_bar)

reset("hard")