import pygame
from utils import resize_img
from random import randint
from instrument import Instrument

class Guitar(Instrument):
    def __init__(self, x, y):
        super().__init__("guitar", x, y)
        self.window = resize_img(pygame.image.load("assets/images/ui/guitar_window.png"), width=32*4)
        self.arrows_img = [resize_img(pygame.image.load(f"assets/images/ui/arrow{i}.png"), width=5*4) for i in range(4)]
        self.sound = [pygame.mixer.Sound(f"assets/sound/instruments/guitar/Guitar_Chord_{i}.mp3") for i in range(1,3)]
        self.last_arrow = 0
        self.arrows = []
        self.points = 0
        self.points_to_win = 10

    def update(self, now, dt, player):
        super().update(now, dt, player)
        if self.playing:
            if now - self.last_arrow >= randint(5, 10) / 10:
                self.last_arrow = now
                self.arrows.append([randint(0, 3), 2*4])

            despawn_idx = -1
            for i, arrow in enumerate(self.arrows):
                arrow[1] += 100 * dt
                if arrow[1] >= 32 * 4 + 5 * 4:
                    despawn_idx = i

            if despawn_idx != -1:
                self.arrows.pop(despawn_idx)
                self.points = max(0, self.points - 1)

    def draw(self, screen, player):
        super().draw(screen, player)
        if self.playing:
            screen.blit(self.window, (self.rect.x - 40, self.rect.y - 40))
            for arrow in self.arrows:
                screen.blit(self.arrows_img[arrow[0]], (self.rect.x - 40 + 3 * 4 + 7 * 4 * arrow[0], self.rect.y - 40 + 32 * 4 - arrow[1]))
            
            pygame.draw.rect(screen, (0, 0, 0), (self.rect.x - 40, self.rect.y - 40 - 25, 32*4, 20))
            pygame.draw.rect(screen, (255, 255, 255), (self.rect.x - 36, self.rect.y - 36 - 25, 32*4 - 8, 12))
            pygame.draw.rect(screen, (0, 255, 0), (self.rect.x - 36, self.rect.y - 36 - 25, (32*4 - 8) * self.points / self.points_to_win, 12))

    def handle_input(self, key):
        keys = [pygame.K_LEFT, pygame.K_DOWN, pygame.K_UP, pygame.K_RIGHT]
        if not key in keys:
            return False
        key_i = keys.index(key)
        for arrow in self.arrows:
            if arrow[0] == key_i and 32*4 - 25 <= arrow[1] <= 32*4 - 5:
                self.arrows.remove(arrow)
                self.points += 1
                self.sound[randint(0, 1)].play()
                if self.points >= self.points_to_win:
                    self.playing = False
                    self.points = 0
                    return True
            else:
                self.points = max(0, self.points - 1)
        return False