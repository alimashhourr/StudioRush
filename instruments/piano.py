import pygame
from utils import resize_img
from random import randint
from instrument import Instrument

class Piano(Instrument):
    def __init__(self, x, y):
        super().__init__("piano", x, y)
        key = ["do", "re", "mi", "fa", "sol", "la", "ti", "doo"]	
        self.window = resize_img(pygame.image.load("assets/images/ui/piano_window.png"), width=32*4)
        self.sound = {}
        for i in range(8):
            self.sound[key[i]] = pygame.mixer.Sound(f"assets/sound/instruments/piano/{key[i]}.mp3")
            self.sound[key[i]].set_volume(0.8)
        self.tiles_img = [resize_img(pygame.image.load(f"assets/images/ui/tile{i}.png"), width=5*4) for i in range(2)]
        self.melody = ["mi", "fa", "sol", "la", "ti", "do", "re", "mi", "fa", "sol", "la", "ti", "do", "re", "mi"]
        self.keynum = 0
        self.last_tile = 0
        self.next_tile_interval = 0
        self.tiles = []
        self.points = 0
        self.points_to_win = 10

    def play(self):
        if not self.playing:
            # Reset le pointage
            self.points = 0
            self.tiles = []
        super().play()

    def update(self, now, dt, player):
        super().update(now, dt, player)
        if self.playing:
            if now - self.last_tile >= self.next_tile_interval:
                self.last_tile = now
                self.tiles.append([randint(0, 3), 2*4, randint(0, 1)])
                self.next_tile_interval = randint(8, 12) / 10

            despawn_idx = -1
            for i, tile in enumerate(self.tiles):
                tile[1] += 100 * dt
                if tile[1] >= 32 * 4 + 2 * 4:
                    despawn_idx = i

            if despawn_idx != -1:
                self.tiles.pop(despawn_idx)
                self.points = max(0, self.points - 1)

    def draw(self, screen, player):
        super().draw(screen, player)
        if self.playing:
            screen.blit(self.window, (self.rect.x - 40, self.rect.y - 40))
            for tile in self.tiles:
                screen.blit(self.tiles_img[tile[2]], (self.rect.x - 40 + 3 * 4 + 7 * 4 * tile[0], self.rect.y - 40 + tile[1] - 8 * 4))
            
            pygame.draw.rect(screen, (0, 0, 0), (self.rect.x - 40, self.rect.y - 40 - 25, 32*4, 20))
            pygame.draw.rect(screen, (255, 255, 255), (self.rect.x - 36, self.rect.y - 36 - 25, 32*4 - 8, 12))
            pygame.draw.rect(screen, (0, 255, 0), (self.rect.x - 36, self.rect.y - 36 - 25, (32*4 - 8) * self.points / self.points_to_win, 12))

    def handle_input(self, key):
        keys = [pygame.K_LEFT, pygame.K_DOWN, pygame.K_UP, pygame.K_RIGHT]
        if not key in keys:
            return False
        key_i = keys.index(key)
        for tile in self.tiles:
            if tile[0] == key_i and 32*4 - 75 <= tile[1] <= 32*4 + 20:
                self.tiles.remove(tile)
                self.points += 1
                self.sound[self.melody[self.keynum]].play()
                self.keynum += 1
                if self.keynum >= len(self.melody):
                    self.keynum = 0
                if self.points >= self.points_to_win:
                    self.playing = False
                    return True
            else:
                self.points = max(0, self.points - 1)
        return False