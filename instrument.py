import pygame
from utils import resize_img

class Instrument():
    def __init__(self, name, x, y):
        self.name = name
        self.img = pygame.image.load(f"assets/images/instruments/{name}.png")
        self.img_hover = pygame.image.load(f"assets/images/instruments/{name}_hover.png")
        self.rect = self.img.get_rect(x=x, y=y)

        self.playing = False
        self.window = resize_img(pygame.image.load("assets/images/ui/guitar_window.png"), width=32*4)

    def update(self):
        if self.playing:
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