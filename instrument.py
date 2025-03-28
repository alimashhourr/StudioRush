import pygame
from utils import resize_img

class Instrument():
    def __init__(self, name, x, y):
        self.name = name
        self.img = pygame.image.load(f"assets/images/instruments/{name}.png")
        self.img_hover = pygame.image.load(f"assets/images/instruments/{name}_hover.png")
        self.rect = self.img.get_rect(x=x, y=y)
        self.playing = False

    def draw(self, screen, players):
        if self.rect.colliderect(players[0].rect) or (len(players) == 2 and self.rect.colliderect(players[1].rect)):
            screen.blit(self.img_hover, self.rect)
        else:
            screen.blit(self.img, self.rect)
    
    def play(self):
        self.playing = True

    def stop_playing(self):
        self.playing = False
    
    def draw_interface(self, screen):
        pass

    def update(self, now, dt):
        pass
    
    def handle_input(self, key, player): # renvoie True si le minijeu est gagné
        pass