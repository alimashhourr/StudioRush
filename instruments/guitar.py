import pygame
from utils import resize_img
from random import randint
from instrument import Instrument

class Guitar(Instrument):
    def __init__(self, x, y):
        super().__init__("guitar", x, y)
        self.window = resize_img(pygame.image.load("assets/images/ui/guitar_window.png"), width=32*4)
        self.arrows_img = [resize_img(pygame.image.load(f"assets/images/ui/arrow{i}.png"), width=5*4) for i in range(4)]
        self.sound = [pygame.mixer.Sound(f"assets/sound/instruments/guitar/guitar{i}.mp3") for i in range(4)]
        for i in range(4):
            self.sound[i].set_volume(0.3)
        self.last_arrow = 0
        self.next_arrow_interval = 0
        self.arrows = []
        self.points = 0
        self.points_to_win = 6

    def play(self):
        if not self.playing:
            # Reset le pointage
            self.points = 0
            self.arrows = []
        super().play()

    def update(self, now, dt):
        super().update(now, dt)
        if self.playing:
            if now - self.last_arrow >= self.next_arrow_interval:
                self.last_arrow = now
                self.arrows.append([randint(0, 3), 2*4])
                self.next_arrow_interval = randint(4, 9) / 10

            despawn_idx = -1
            for i, arrow in enumerate(self.arrows):
                arrow[1] += 100 * dt
                if arrow[1] >= 32 * 4 + 5 * 4:
                    despawn_idx = i

            if despawn_idx != -1:
                self.arrows.pop(despawn_idx)
                self.points = max(0, self.points - 1)

    def draw_interface(self, screen):
        screen.blit(self.window, (self.rect.x - 40, self.rect.y - 40))
        for arrow in self.arrows:
            screen.blit(self.arrows_img[arrow[0]], (self.rect.x - 40 + 3 * 4 + 7 * 4 * arrow[0], self.rect.y - 40 + 32 * 4 - arrow[1]))
        
        pygame.draw.rect(screen, (0, 0, 0), (self.rect.x - 40, self.rect.y - 40 - 25, 32*4, 20))
        pygame.draw.rect(screen, (255, 255, 255), (self.rect.x - 36, self.rect.y - 36 - 25, 32*4 - 8, 12))
        pygame.draw.rect(screen, (0, 255, 0), (self.rect.x - 36, self.rect.y - 36 - 25, (32*4 - 8) * self.points / self.points_to_win, 12))

    def handle_input(self, key, player):
        keys = [player.keybinds['left'], player.keybinds['down'], player.keybinds['up'], player.keybinds['right']]
        if not key in keys:
            return False
        key_i = keys.index(key)
        for arrow in self.arrows:
            if arrow[0] == key_i and 32*4 - 30 <= arrow[1] <= 32*4 + 10:
                self.arrows.remove(arrow)
                self.points += 1
                self.sound[arrow[0]].play()
                if self.points >= self.points_to_win:
                    self.playing = False
                    player.playing = False
                    return True
            else:
                self.points = max(0, self.points - 1)
        return False