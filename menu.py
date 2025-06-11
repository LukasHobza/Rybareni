import pygame
import sys
import functions as fce
import json
import os
import config as conf  # <-- Import sdílených proměnných
import tile_manager as tilem

SAVE_DIR = "saves"
os.makedirs(SAVE_DIR, exist_ok=True)
menu_img = pygame.transform.scale(pygame.image.load(fce.get_path("res/menuHry.png")),(conf.screen_width, conf.screen_height))

pygame.init()
pixel_font = pygame.font.Font(fce.get_path("res/font/Minecraftia-Regular.ttf"), 42)
WHITE = (255, 255, 255)
BLUE = (100, 100, 255)
FONT = pygame.font.SysFont("Arial", 48, bold=True)

menu_items = ["new game", "continue", "exit"]
selected_index = 0
submenu_state = None
slot_names = [None, None, None]  # 3 herní sloty
selected_slot = 0

input_active = False
slot_input = ""
confirm_overwrite = False


def get_slot_path(slot_index):
    return os.path.join(SAVE_DIR, f"slot{slot_index}.json")


def save_game(slot_index, player):
    data = {
        "name": slot_names[slot_index],
        "inventory": conf.inventory,
        "level": player.level,
        "hp": player.hp,
        "positionX": player.pos.x,
        "positionY": player.pos.y,
        "mapX": conf.cur_map.x,
        "mapY": conf.cur_map.y,
        "coins": conf.coins
    }
    with open(get_slot_path(slot_index), "w") as f:
        json.dump(data, f)


def load_game(slot_index, player):
    path = get_slot_path(slot_index)
    if os.path.exists(path):
        with open(path, "r") as f:
            data = json.load(f)
            conf.inventory = data.get("inventory", [])
            player.level = data.get("level", 1)
            player.hp = data.get("hp", 100)
            player.pos.x = data.get("positionX", 400)
            player.pos.y = data.get("positionY", 400)
            conf.cur_map.x = data.get("mapX", 5)
            conf.cur_map.y = data.get("mapY", 5)
            conf.coins = data.get("coins", 6)


# === NAČTI JMÉNA SLOTŮ ===
for i in range(3):
    path = get_slot_path(i)
    if os.path.exists(path):
        with open(path, "r") as f:
            data = json.load(f)
            slot_names[i] = data.get("name")


def draw_menu(win):
    win.blit(menu_img,(0,0))
    title = pixel_font.render("nazev hry", True, BLUE)
    win.blit(title, (win.get_width() // 2 - title.get_width() // 2, 50))

    if submenu_state is None:
        for i, text in enumerate(menu_items):
            label = FONT.render(text, True, BLUE)
            x = win.get_width() // 2 - label.get_width() // 2
            y = 200 + i * 80
            win.blit(label, (x, y))
            if i == selected_index:
                arrow = FONT.render(">", True, BLUE)
                win.blit(arrow, (x - 50, y))

    elif submenu_state in ["new_game", "continue"]:
        subtitle = pixel_font.render("Vyber slot:", True, BLUE)
        win.blit(subtitle, (win.get_width() // 2 - subtitle.get_width() // 2, 120))

        for i in range(3):
            name = slot_names[i] if slot_names[i] else "--- prázdný slot ---"
            label = FONT.render(f"Slot {i+1}: {name}", True, BLUE)
            x = win.get_width() // 2 - label.get_width() // 2
            y = 200 + i * 80
            win.blit(label, (x, y))
            if i == selected_slot:
                arrow = FONT.render(">", True, BLUE)
                win.blit(arrow, (x - 50, y))

        if confirm_overwrite:
            prompt = FONT.render("Slot je obsazený. Přejmenovat? ENTER = Ano, ESC = Ne", True, BLUE)
            win.blit(prompt, (win.get_width() // 2 - prompt.get_width() // 2, 480))

        elif input_active:
            prompt = FONT.render("Zadej jméno slotu:", True, BLUE)
            text_surface = FONT.render(slot_input, True, BLUE)
            win.blit(prompt, (win.get_width() // 2 - prompt.get_width() // 2, 480))
            win.blit(text_surface, (win.get_width() // 2 - text_surface.get_width() // 2, 540))


def handle_menu_input(event,player):
    global selected_index, submenu_state, selected_slot, slot_names
    global input_active, slot_input, confirm_overwrite

    if confirm_overwrite:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                confirm_overwrite = False
                input_active = True
                slot_input = ""
            elif event.key == pygame.K_ESCAPE:
                confirm_overwrite = False
        return None

    if input_active:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                slot_names[selected_slot] = slot_input
                input_active = False
                submenu_state = None
                conf.cur_save_slot = selected_slot
                fce.reset(player)
                #save_game(selected_slot, player)
                conf.gamemode = conf.GAMEMODE_GAME
                return "start_new_game"
            elif event.key == pygame.K_BACKSPACE:
                slot_input = slot_input[:-1]
            else:
                if len(slot_input) < 12:
                    slot_input += event.unicode
        return None

    if submenu_state is None:
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_s, pygame.K_DOWN]:
                selected_index = (selected_index + 1) % len(menu_items)
            elif event.key in [pygame.K_w, pygame.K_UP]:
                selected_index = (selected_index - 1) % len(menu_items)
            elif event.key == pygame.K_RETURN:
                choice = menu_items[selected_index]
                if choice == "exit":
                    pygame.quit()
                    sys.exit()
                elif choice == "new game":
                    submenu_state = "new_game"
                elif choice == "continue":
                    submenu_state = "continue"
    else:
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_s, pygame.K_DOWN]:
                selected_slot = (selected_slot + 1) % 3
            elif event.key in [pygame.K_w, pygame.K_UP]:
                selected_slot = (selected_slot - 1) % 3
            elif event.key == pygame.K_ESCAPE:
                submenu_state = None
            elif event.key == pygame.K_RETURN:
                if submenu_state == "new_game":
                    if slot_names[selected_slot] is not None:
                        confirm_overwrite = True
                    else:
                        input_active = True
                        slot_input = ""
                elif submenu_state == "continue":
                    if slot_names[selected_slot] is not None:
                        conf.cur_save_slot = selected_slot
                        load_game(selected_slot,player)

                        conf.cur_map_data = tilem.load_map(f"map{int(conf.cur_map.x)}{int(conf.cur_map.y)}.txt") #nacte zakladni mapu
                        tilem.map_surface = tilem.generate_map_surface(tilem.load_map(f"map{int(conf.cur_map.x)}{int(conf.cur_map.y)}.txt")) #vygeneruje 
                        
                        submenu_state = None
                        conf.gamemode = conf.GAMEMODE_GAME
                        return "load_game"
    return None
