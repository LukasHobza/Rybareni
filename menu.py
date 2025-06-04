import pygame
import sys
import functions as fce
import json
import os
import config as conf

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


SAVE_FOLDER = "saves"
os.makedirs(SAVE_FOLDER, exist_ok=True)

def get_save_path(slot_index):
    return os.path.join(SAVE_FOLDER, f"slot_{slot_index}.json")

def save_game(slot_index,player):
    data = {
        "inventory": conf.inventory,
        "level": player.level,
        "positionX": player.pos.x,
        "positionY": player.pos.y,
        "mapX": conf.cur_map.x,
        "mapY": conf.cur_map.y
    }
    with open(get_save_path(slot_index), "w") as f:
        json.dump(data, f)

def load_game(slot_index,player):
    try:
        with open(get_save_path(slot_index), "r") as f:
            data = json.load(f)
            conf.inventory = data.get("inventory", [])
            player.level = data.get("level", 1)
            player.pos.x = data.get("positionX", (0, 0))
            player.pos.y = data.get("positionY", (0, 0))
            conf.cur_map.x = data.get("mapX", 5)
            conf.cur_map.y = data.get("mapY", 5)
            return True
    except FileNotFoundError:
        return False

def draw_menu(win):
    win.fill(WHITE)
    title = pixel_font.render("nazev hry", True, BLUE)
    win.blit(title, (win.get_width() // 2 - title.get_width() // 2, conf.TILE_SIZE))

    if submenu_state is None:
        for i, text in enumerate(menu_items):
            label = FONT.render(text, True, BLUE)
            x = win.get_width() // 2 - label.get_width() // 2
            y = conf.TILE_SIZE * 4 + i * conf.TILE_SIZE * 2
            win.blit(label, (x, y))
            if i == selected_index:
                arrow = FONT.render(">", True, BLUE)
                win.blit(arrow, (x - conf.TILE_SIZE, y))

    elif submenu_state in ["new_game", "continue"]:
        subtitle = pixel_font.render("Vyber slot:", True, BLUE)
        win.blit(subtitle, (win.get_width() // 2 - subtitle.get_width() // 2, conf.TILE_SIZE * 2))

        for i in range(3):
            name = slot_names[i] if slot_names[i] else "--- prázdný slot ---"
            label = FONT.render(f"Slot {i+1}: {name}", True, BLUE)
            x = win.get_width() // 2 - label.get_width() // 2
            y = conf.TILE_SIZE * 4 + i * conf.TILE_SIZE * 2
            win.blit(label, (x, y))
            if i == selected_slot:
                arrow = FONT.render(">", True, BLUE)
                win.blit(arrow, (x - conf.TILE_SIZE, y))

        if confirm_overwrite:
            prompt = FONT.render("Slot je obsazený. Přejmenovat? ENTER = Ano, ESC = Ne", True, BLUE)
            win.blit(prompt, (win.get_width() // 2 - prompt.get_width() // 2, conf.TILE_SIZE * 13))

        elif input_active:
            prompt = FONT.render("Zadej jméno slotu:", True, BLUE)
            text_surface = FONT.render(slot_input, True, BLUE)
            win.blit(prompt, (win.get_width() // 2 - prompt.get_width() // 2, conf.TILE_SIZE * 13))
            win.blit(text_surface, (win.get_width() // 2 - text_surface.get_width() // 2, conf.TILE_SIZE * 14))

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
                #save_game(selected_slot,player)  # Uložení nového progresu
                fce.reset(player)
                conf.cur_save_slot = selected_slot
                conf.gamemode = conf.GAMEMODE_GAME
                return "start_new_game"  # <<< ZDE spustit novou hru
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
                        submenu_state = None
                        if load_game(selected_slot,player):
                            return "load_game"  # <<< ZDE načíst existující uloženou hru
    return None
