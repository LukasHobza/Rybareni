import pygame

class Item:
    def __init__(self, x,y, map):
        self.pos = pygame.Vector2(x,y)
        self.pick_up = True
        self.map = map
        self.dropped_item_delay = 0

    def draw(self, window):
        """Vykresli item."""
        if self.dropped_item_delay > 0:
            self.dropped_item_delay -= 1

        window.blit(self.img, (self.pos))

    def use():
        pass

    def interact():
        pass

    def to_dict(self):
        return {
            'name': self.name,
            'pos_x': self.pos.x,
            'pos_y': self.pos.y,
            'map_x': self.map.x,
            'map_y': self.map.y
        }