#kvuli fulscreenu
import os
os.environ['SDL_VIDEO_ALLOW_HIGHDPI'] = '1'

import pygame, ctypes

def get_scaling_factor():
    user32 = ctypes.windll.user32
    gdi32 = ctypes.windll.gdi32
    user32.SetProcessDPIAware()  # Řekni OS, že chceme nativní DPI
    dc = user32.GetDC(0)
    dpi = gdi32.GetDeviceCaps(dc, 88)  # 88 = LOGPIXELSX
    user32.ReleaseDC(0, dc)
    return dpi / 96  # 96 DPI je standardní 100%
scale_factor = get_scaling_factor()

pygame.init()

ROWS = 19
COLS = 33 #max 35 vic ne

MAP_WIDTH_IN_TILES = COLS+1 #+1 kvuli inventari na boku
MAP_HEIGHT_IN_TILES = ROWS+0 

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
screen_width = int(screen_width / scale_factor)
screen_height = int(screen_height / scale_factor)

tile_width = screen_width // MAP_WIDTH_IN_TILES
tile_height = screen_height // MAP_HEIGHT_IN_TILES
TILE_SIZE = round(min(tile_width, tile_height)* scale_factor)

map_pixel_width = TILE_SIZE * MAP_WIDTH_IN_TILES
map_pixel_height = TILE_SIZE * MAP_HEIGHT_IN_TILES
offset_x = (screen_width - map_pixel_width) // 2
offset_y = (screen_height - map_pixel_height) // 2

#CONFIG
items = []
debug = False

#tilemap
last_solid = 18

#gamemody
gamemode = 3
GAMEMODE_GAME = 0
GAMEMODE_SHOP = 1
GAMEMODE_FISH_MINIGAME = 2
GAMEMODE_MENU = 3

#veci pro mapu
map_data_ = []
cur_map = pygame.Vector2(5,5)
cur_map_data = []

#veci pro inventar
inv_pos = 0
inventory = []

entities = []

#veci pro obchod
shop_pos = 0
shop_delay = 0
coins = 50

#rybareni
water_lake = 1
water_river = 2
water_ocean = 3

cur_save_slot = 0