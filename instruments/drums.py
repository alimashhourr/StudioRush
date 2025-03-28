import pygame
from utils import resize_img
from instrument import Instrument
import math

class Drums(Instrument):
    def __init__(self, x, y):
        super().__init__("drums", x, y)
        self.circle_img = resize_img(pygame.image.load("assets/images/ui/drums_circle.png"), width=32*2.2)
        self.cursor_img = resize_img(pygame.image.load("assets/images/ui/drums_cursor.png"), width=6*2.2)
        
        self.cursor_rect = self.cursor_img.get_rect()
        self.circle_radius = self.circle_img.get_width()/2
        self.cursor_radius_coef = 0.7

        self.cursors_angle = [90]*3
        self.current_cursor = 0

        self.sound = [pygame.mixer.Sound(f"assets/sound/instruments/drums/drums{i}.mp3") for i in range(3)]
        for i in range(3):
            self.sound[i].set_volume(0.8)
    
    def play(self):
        if not self.playing:
            # Reset les cercles
            self.current_cursor = 0
            self.cursors_angle = [90]*3
            self.just_started = True
        super().play()

    def update(self, now, dt):
        super().update(now, dt)
        if self.playing:
            self.cursors_angle[self.current_cursor] += 300 * dt

    def draw_interface(self, screen):
        for i, angle in enumerate(self.cursors_angle):
            circle_x = self.rect.x + 50 + 80*i
            circle_y = self.rect.y - 50
            screen.blit(self.circle_img, (circle_x, circle_y))

            cursor_x = circle_x + (math.cos(math.radians(angle)) + 1) * self.circle_radius*self.cursor_radius_coef + self.circle_radius * (1 - self.cursor_radius_coef)
            cursor_y = circle_y + (math.sin(math.radians(angle)) + 1) * self.circle_radius*self.cursor_radius_coef + self.circle_radius * (1 - self.cursor_radius_coef)
            rotated_cursor = pygame.transform.rotate(self.cursor_img, -angle - 90)
            self.cursor_rect = rotated_cursor.get_rect(center=(cursor_x, cursor_y))

            screen.blit(rotated_cursor, self.cursor_rect)

    def handle_input(self, key, player):
        if key == player.keybinds['up']:
            if 270-18 < (self.cursors_angle[self.current_cursor] % 360) < 270+18:
                self.sound[self.current_cursor].play()
                self.current_cursor += 1
                if self.current_cursor == 3:
                    self.playing = False
                    player.playing = False
                    return True
            else:
                self.playing = False
                player.playing = False
        return False