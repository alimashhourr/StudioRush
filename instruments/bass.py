import pygame
from instrument import Instrument

class Bass(Instrument):
    def __init__(self, x, y):
        super().__init__("bass", x, y)
    
        self.lines_height = 15
        self.lines_spacing = 20
        self.lines_width = 150
        self.cursor_width = 8
        
        self.lines_x = self.rect.centerx-self.lines_width//2
        self.lines_y = y+160
        
        self.current_cursor = 0
        self.cursor_dir = 1
        self.cursors_pos = [0]*4

        self.just_started = False

        self.sound = [pygame.mixer.Sound(f"assets/sound/instruments/bass/bass{i}.mp3") for i in range(4)]
        for i in range(3):
            self.sound[i].set_volume(0.8)
    
    def play(self):
        if not self.playing:
            self.current_cursor = 0
            self.cursors_pos = [0]*4
            self.just_started = True
        super().play()

    def update(self, now, dt, player):
        super().update(now, dt, player)
        if self.playing:
            self.cursors_pos[self.current_cursor] += 160 * dt * self.cursor_dir
            if self.cursors_pos[self.current_cursor] > self.lines_width - self.cursor_width:
                self.cursors_pos[self.current_cursor] = self.lines_width - self.cursor_width
                self.cursor_dir *= -1
            if self.cursors_pos[self.current_cursor] < 0:
                self.cursors_pos[self.current_cursor] = 0
                self.cursor_dir *= -1

    def draw(self, screen, player):
        super().draw(screen, player)
        if self.playing:
            for i, pos in enumerate(self.cursors_pos):
                pygame.draw.rect(screen, (255, 255, 255), (self.lines_x, self.lines_y+i*self.lines_spacing, self.lines_width, self.lines_height))
                pygame.draw.rect(screen, (165, 165, 165), (self.lines_x + self.lines_width//2 - self.cursor_width//2, self.lines_y + i*self.lines_spacing, self.cursor_width, self.lines_height))
                pygame.draw.rect(screen, (77, 77, 77), (self.lines_x + pos, self.lines_y + i*self.lines_spacing, self.cursor_width, self.lines_height))

    def handle_input(self, key):
        if key == pygame.K_SPACE:
            if self.just_started: # La barre espace est pressée pour lancer le jeu
                self.just_started = False
                return False
            
            if self.lines_width//2 - self.cursor_width//2 - 3 < (self.cursors_pos[self.current_cursor]) < self.lines_width//2 + self.cursor_width//2 + 3:
                self.sound[self.current_cursor].play()
                self.current_cursor += 1
                if self.current_cursor >= 4:
                    self.playing = False
                    return True
            else:
                self.playing = False
        return False