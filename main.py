import pygame,sys
import player as p
import config as conf
import tile_manager as tilem
from entities import fish_blue_slime
from items import basic_fishing_rod
from items import iron_sword
from items import iron_axe
import functions as fce
import ui
import inventory as inv
import shop
from items import shop_object
import fish_minigame
import menu

WIDTH, HEIGHT = conf.TILE_SIZE * conf.COLS,conf.TILE_SIZE * conf.ROWS + conf.TILE_SIZE #sirka, vyska okna
WIN = pygame.display.set_mode((0,0),pygame.FULLSCREEN) #herni okno
pygame.display.set_caption("Rabářnická hra")

def main():
    """Hlavni funkce."""
    clock = pygame.time.Clock()
    run = True
    FPS = 60

    player = p.Player(conf.TILE_SIZE*9,conf.TILE_SIZE*9,5)

    def call_mouse_event_functions(event):
        """Vola fce ktere pracuji s mysi."""
        if conf.gamemode == conf.GAMEMODE_GAME:
            inv.manager(event)
        if conf.gamemode == conf.GAMEMODE_SHOP:
            shop.manager(event)
        if conf.gamemode == conf.GAMEMODE_MENU:
            pass

    def call_event_functions(event):
        """Vola fce ktere pracuji s event."""
        if conf.gamemode == conf.GAMEMODE_SHOP:
            shop.buy_item(event)
            shop.close_shop(event)
        if conf.gamemode == conf.GAMEMODE_GAME:
            fce.drop_item(event,player)
            fce.use_item(event,player)
        if conf.gamemode == conf.GAMEMODE_MENU:
            menu.handle_menu_input(event, player) #menu event
        fce.debug(event)

    def call_functions():
        """Vola fce."""
        if conf.gamemode == conf.GAMEMODE_GAME:
            shop.shop_delay_manager()
            fce.pick_up_check(player)
            fce.map_escape_check(player)
            fce.check_hit(player, conf.entities)
        if conf.gamemode == conf.GAMEMODE_FISH_MINIGAME:
            fish_minigame.manager(player,conf.entities)
        if conf.gamemode == conf.GAMEMODE_MENU:
            pass

    def redraw_window():
        """Prekresluje herni okno."""
        WIN.fill((0,0,0))
        if conf.gamemode == conf.GAMEMODE_GAME or conf.gamemode == conf.GAMEMODE_SHOP or conf.gamemode == conf.GAMEMODE_FISH_MINIGAME:
            tilem.draw_map(WIN)

            for item in conf.items: #projede vsechny itemy
                if item.map == conf.cur_map: #kresli jen ty na aktualni mape
                    item.draw(WIN)

            for entity in conf.entities: #projede vsechny entity
                if entity.map == conf.cur_map: #kresli jen ty na aktualni mape
                    entity.draw(WIN)
                    entity.draw_hp_bar(WIN)
                    if conf.debug:
                        entity.draw_debug_path(WIN)

            player.draw(WIN)
            ui.draw(WIN,player.hp,player.max_hp)
            inv.draw(WIN)
        if conf.gamemode == conf.GAMEMODE_SHOP:
            shop.draw(WIN)
        if conf.gamemode == conf.GAMEMODE_FISH_MINIGAME:
            fish_minigame.draw(WIN)
        if conf.gamemode == conf.GAMEMODE_MENU:
            menu.draw_menu(WIN) #menu vykreslení

        pygame.display.update()

    def move():
        """Vola pohyb vsech entit vcetne hrace."""
        if conf.gamemode == conf.GAMEMODE_GAME:
            player.manager(dt)
            for entity in conf.entities[:]:
                if entity.map == conf.cur_map:
                    fce.map_escape_check(entity)
                    entity.move(player,dt)
                    if entity.hp <= 0:
                        entity.drop_item()
                        conf.entities.remove(entity)

    #jen tohle je herní smyčka :)
    while run:
        dt = clock.tick(FPS) / 1000 

        move()
        redraw_window()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #kdyby to tu nebylo tak to nejde normalne zavrit
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEWHEEL:
                call_mouse_event_functions(event)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_p:
                    menu.save_game(conf.cur_save_slot,player)
            call_event_functions(event)
        call_functions()

        #print(dt)
        print(conf.cur_map)
        #fce.show_cords(player) #vypisuje souradky hrace

main()