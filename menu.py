import pygame
import sys
import functions as fce
import config as conf

pixel_font = pygame.font.Font(fce.get_path("res/font/Minecraftia-Regular.ttf"), 42)
WHITE = (255, 255, 255)
BLUE = (100, 100, 255)
FONT = pixel_font

menu_items = ["new game", "continue", "exit"]
selected_index = 0
submenu_state = None
slot_names = [None, None, None]  # 3 herní sloty
selected_slot = 0

input_active = False
slot_input = ""
confirm_overwrite = False




def draw_menu(win):
    win.fill(WHITE)
    title = pixel_font.render("nazev hry", True, BLUE)
    win.blit(title, (win.get_width() // 2 - title.get_width() // 2, conf.TILE_SIZE))

    if submenu_state is None:
        for i, text in enumerate(menu_items):
            label = FONT.render(text, True, BLUE)
            x = win.get_width() // 2 - label.get_width() // 2
            y = conf.TILE_SIZE * 3 + i * conf.TILE_SIZE * 2 // 1.5
            win.blit(label, (x, int(y)))
            if i == selected_index:
                arrow = FONT.render(">", True, BLUE)
                win.blit(arrow, (x - conf.TILE_SIZE, int(y)))

    elif submenu_state in ["new_game", "continue"]:
        subtitle = pixel_font.render("Vyber slot:", True, BLUE)
        win.blit(subtitle, (win.get_width() // 2 - subtitle.get_width() // 2, int(conf.TILE_SIZE * 2)))

        for i in range(3):
            name = slot_names[i] if slot_names[i] else "--- prázdný slot ---"
            label = FONT.render(f"Slot {i+1}: {name}", True, BLUE)
            x = win.get_width() // 2 - label.get_width() // 2
            y = conf.TILE_SIZE * 4 + i * conf.TILE_SIZE * 2 // 1.5
            win.blit(label, (x, int(y)))
            if i == selected_slot:
                arrow = FONT.render(">", True, BLUE)
                win.blit(arrow, (x - conf.TILE_SIZE, int(y)))

        if confirm_overwrite:
            prompt = FONT.render("Slot je obsazený. Přejmenovat? ENTER = Ano, ESC = Ne", True, BLUE)
            win.blit(prompt, (win.get_width() // 2 - prompt.get_width() // 2, int(conf.TILE_SIZE * 10)))

        elif input_active:
            prompt = FONT.render("Zadej jméno slotu:", True, BLUE)
            text_surface = FONT.render(slot_input, True, BLUE)
            win.blit(prompt, (win.get_width() // 2 - prompt.get_width() // 2, int(conf.TILE_SIZE * 10)))
            win.blit(text_surface, (win.get_width() // 2 - text_surface.get_width() // 2, int(conf.TILE_SIZE * 11)))


def handle_menu_input(event):
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
                        return "load_game"  # <<< ZDE načíst existující uloženou hru
    return None