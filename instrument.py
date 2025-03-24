import pygame
from utils import resize_img
from random import randint

class Instrument():
    def __init__(self, name, x, y):
        self.name = name
        self.img = pygame.image.load(f"assets/images/instruments/{name}.png")
        self.img_hover = pygame.image.load(f"assets/images/instruments/{name}_hover.png")
        self.rect = self.img.get_rect(x=x, y=y)

        self.playing = False
        self.window = resize_img(pygame.image.load("assets/images/ui/guitar_window.png"), width=32*4)
        self.arrows_img = [resize_img(pygame.image.load(f"assets/images/ui/arrow{i}.png"), width=5*4) for i in range(4)]
        self.last_arrow = 0.0
        self.arrows = [] # (arrow_i, arrow_y) ex. [(2, 15), (3, 10), (2, 12), ...]

    def update(self, now):
        if self.playing:
            print(now - self.last_arrow)
            if now - self.last_arrow >= 2:
                self.last_arrow = now
                self.arrows.append((randint(0, 3), 0))
        for arrows in self.arrows:
            pass
    
    def draw(self, screen, player):
        if self.rect.colliderect(player.rect):
            screen.blit(self.img_hover, self.rect)
        else:
            screen.blit(self.img, self.rect)
        if self.playing:
            screen.blit(self.window, (self.rect.x - 40, self.rect.y - 40))

    def play(self):
        self.playing = True