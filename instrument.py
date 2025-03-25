import pygame
from utils import resize_img
from random import randint

class Instrument():
    def __init__(self, name, x, y):
        self.name = name
        self.img = pygame.image.load(f"assets/images/instruments/{name}.png")
        self.img_hover = pygame.image.load(f"assets/images/instruments/{name}_hover.png")
        self.rect = self.img.get_rect(x=x, y=y)

        # Arrows game
        self.playing = False
        self.window = resize_img(pygame.image.load("assets/images/ui/guitar_window.png"), width=32*4)
        self.arrows_img = [resize_img(pygame.image.load(f"assets/images/ui/arrow{i}.png"), width=5*4) for i in range(4)]
        self.last_arrow = 0.0
        self.arrows = [] # (arrow_i, arrow_y) ex. [(2, 15), (3, 10), (2, 12), ...]
        self.points = 0
        self.points_to_win = 15

    def update(self, now, dt, player):
        if self.playing:
            if now - self.last_arrow >= randint(5, 10)/10:
                self.last_arrow = now
                self.arrows.append([randint(0, 3), 2*4])

            despawn_idx = -1
            for i, arrow in enumerate(self.arrows):
                arrow[1] += 100*dt
                if arrow[1] >= 32*4 + 5*4:
                    despawn_idx = self.arrows.index(arrow)
            
            if despawn_idx != -1:
                self.arrows.pop(despawn_idx)
                self.points -= 1
                if self.points < 0:
                    self.points = 0
            
            if not self.rect.colliderect(player.rect):
                self.playing = False
    
    def draw(self, screen, player):
        if self.rect.colliderect(player.rect):
            screen.blit(self.img_hover, self.rect)
        else:
            screen.blit(self.img, self.rect)

        if self.playing:
            screen.blit(self.window, (self.rect.x - 40, self.rect.y - 40))
            for arrow in self.arrows:
                screen.blit(self.arrows_img[arrow[0]], (self.rect.x - 40 + 3*4 + 7*4*arrow[0], self.rect.y - 40 + 32*4 - arrow[1]))
            
            # draw points as progress bar
            pygame.draw.rect(screen, (0, 0, 0), (self.rect.x - 40, self.rect.y - 40 - 25, 32*4, 20)) # black border
            pygame.draw.rect(screen, (255, 255, 255), (self.rect.x - 36, self.rect.y - 36 - 25, 32*4 - 8, 12)) # white background
            pygame.draw.rect(screen, (0, 255, 0), (self.rect.x - 36, self.rect.y - 36 - 25, (32*4 - 8)*self.points/self.points_to_win, 12)) # green progress bar

    def play(self):
        self.playing = True
        self.points = 0
        self.arrows = []
    
    def arrow_key(self, key_i):
        # Check if the arrow is at the right y position
        for arrow in self.arrows:
            if arrow[0] != key_i:
                continue

            if 32*4 - 25 <= arrow[1] <= 32*4 - 5:
                self.arrows.remove(arrow)
                self.points += 1
                if self.points >= self.points_to_win:
                    self.playing = False
                    self.points = 0
                    return True
            else:
                self.points -= 1
                if self.points < 0:
                    self.points = 0
            break
        return False