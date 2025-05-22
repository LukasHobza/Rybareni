import pygame
import sys

# Inicializace pygame
pygame.init()

# Rozměry okna
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")

# Barvy a fonty
WHITE = (255, 255, 255)
BLUE = (100, 100, 255)
FONT = pygame.font.SysFont("arial", 50, bold=True)

# Položky menu
menu_items = ["new game", "continue", "exit"]
selected_index = 0

def draw_menu():
    screen.fill(WHITE)

    # Titulek
    title_font = pygame.font.SysFont("arial", 70, bold=True)
    title_surf = title_font.render("nazev hry", True, BLUE)
    screen.blit(title_surf, ((WIDTH - title_surf.get_width()) // 2, 50))

    # Položky menu
    start_y = 200
    for i, item in enumerate(menu_items):
        color = BLUE
        text_surf = FONT.render(item, True, color)
        x = (WIDTH - text_surf.get_width()) // 2
        y = start_y + i * 80
        screen.blit(text_surf, (x, y))

        # Znak >
        if i == selected_index:
            arrow_surf = FONT.render(">", True, BLUE)
            screen.blit(arrow_surf, (x - 40, y))

# Hlavní smyčka
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_s, pygame.K_DOWN]:
                selected_index = (selected_index + 1) % len(menu_items)
            elif event.key in [pygame.K_w, pygame.K_UP]:
                selected_index = (selected_index - 1) % len(menu_items)
            elif event.key == pygame.K_RETURN:
                print(f"Selected: {menu_items[selected_index]}")
                if menu_items[selected_index] == "exit":
                    pygame.quit()
                    sys.exit()

    draw_menu()
    pygame.display.flip()
    clock.tick(60)
