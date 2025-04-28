import pygame, os,sys
import config as conf

def get_path(filename):
    """Funkce na cestu k souboru, důležité pro EXE i normální běh."""
    if getattr(sys, 'frozen', False):
        # Program běží jako EXE
        base_path = sys._MEIPASS
    else:
        # Program běží jako normální Python skript
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path, filename)

class Tile:
    def __init__(self, image,collision):
        self.image = image
        self.collision = collision
        self.mask = pygame.mask.from_surface(self.image)

class Map_data:
    def __init__(self, data, x, y):
        self.data = data
        self.x = x
        self.y = y

img_tiles = []

for i in range(71):
    img_name ="rpg_" #vychozi nazev obrazku, potom prejmenovat na neco jinho nez rpg
    if i <= 9: #aby to vypadalo ve stylu rpg_0 a ne rpg_
        img_name+="0"
    img_name +=str(i)+".png" #prida napr rpg_01.png
    img_tiles.append(pygame.transform.scale(pygame.image.load(get_path("res/tiles/"+img_name)),(conf.TILE_SIZE, conf.TILE_SIZE))) #prida obrazek do listu

tiles = []

for i in range(71):
    #prida vsechny ctverce do listu i s kolizi/bez kolize
    if i <= 19:
        tiles.append(Tile(img_tiles[i], True))
    else:
        tiles.append(Tile(img_tiles[i], False))

def load_map(filename):
    """Nacte mapu ze souboru."""
    with open(get_path("res/map/" + filename), "r") as f: #otevre soubor s mapou
        return [list(map(int, filter(None, line.strip().split(',')))) for line in f.readlines()] #nacte mapu nekam, idk ale funguje to

for x in range(10):
    for y in range(10):
        try:
            conf.map_data_.append(Map_data(load_map("map"+str(x)+str(y)+".txt"),x,y)) #nacte vsechny mapy ze slozky
        except:
            continue


def draw_tile(window,tile_id, x, y):
    """Vykresli tile. Pouziva se na vykreslovani na map surface."""
    window.blit(tiles[tile_id].image, (x, y))

def change_map():
    """Zmeni mapu."""
    #vygeneruje novou mapu (cely obrazek mapy), funguje to
    for map_data in conf.map_data_:
        if map_data.x == conf.cur_map.x and map_data.y == conf.cur_map.y:
            return generate_map_surface(map_data.data), map_data.data

def generate_map_surface(map_data_):
    """Vygeneruje mapu."""
    map_surface = pygame.Surface((len(map_data_[0]) * conf.TILE_SIZE, len(map_data_) * conf.TILE_SIZE)) #nove jakoby platno
    for row_idx, row in enumerate(map_data_):
        for col_idx, tile_id in enumerate(row):
            draw_tile(map_surface, tile_id, col_idx * conf.TILE_SIZE, row_idx * conf.TILE_SIZE) #vykresli tile na map_surface, ne na obrazovku
    return map_surface

def draw_map(window):
    """Vykresli mapu."""
    window.blit(map_surface, (0, 0))

conf.cur_map_data = load_map("map55.txt") #nacte zakladni mapu
map_surface = generate_map_surface(load_map("map55.txt")) #vygeneruje 