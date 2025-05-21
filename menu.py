import pygame
import functions as fce
import config as conf

pixel_font = pygame.font.Font(fce.get_path("res/font/Minecraftia-Regular.ttf"), 42) #font, velikost fontu
pos = 1

def draw(window):
    """Vykresli ui."""
    window.fill((100,100,100))

    menu_text = pixel_font.render(f"*MENU*",1,"white") #vytvori hp text, font, barva....
    window.blit(menu_text,(20,pos*conf.TILE_SIZE)) #vykresli hp text

def manager(event):
    global pos
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w:
            pos-=1
        elif event.key == pygame.K_s:
            pos+=1



###################################################################

# ----------------------------
# ZÁKLADNÍ KONSTRUKCE V PYTHONU
# ----------------------------

# Funkce se definuje pomocí 'def'
def ukazka_funkce(jmeno):
    """
    Tato funkce bere jeden argument a pouze ho vrací zpět.
    """
    return jmeno

# Podmínky: if, elif, else
x = 10

if x > 10:
    print("X je větší než 10")
elif x == 10:
    print("X je rovno 10")
else:
    print("X je menší než 10")

# Cyklus for – procházení seznamu
seznam = ["jablko", "banán", "třešeň"]
for ovoce in seznam:
    print("Ovoce:", ovoce)

# Cyklus for s range
for i in range(5):  # range(5) znamená čísla 0 až 4
    print("Číslo:", i)

# While smyčka – opakuje se dokud je podmínka pravdivá
pocitadlo = 0
while pocitadlo < 3:
    print("Pocitadlo:", pocitadlo)
    pocitadlo += 1  # stejný zápis jako pocitadlo = pocitadlo + 1

# Match-case – novější alternativa k if-elif-else (od Python 3.10)
den = "pondělí"

match den:
    case "pondělí":
        print("Začátek týdne.")
    case "pátek":
        print("Téměř víkend.")
    case _:
        print("Běžný den.")

# Try-except – ošetření chyb
try:
    cislo = int("abc")  # pokusí se převést text na číslo, ale selže
except ValueError:
    print("Došlo k chybě: hodnota není číslo.")

# Funkce může mít i výchozí hodnoty parametrů
def pozdrav(jmeno="světe"):
    print(f"Ahoj, {jmeno}!")

pozdrav()           # vypíše: Ahoj, světe!
pozdrav("Petře")    # vypíše: Ahoj, Petře!

# Ukončení skriptu – nic dál už neprovádíme
pass  # 'pass' je klíčové slovo, které dělá "nic" – užitečné jako zástupce
