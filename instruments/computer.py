import pygame
from instrument import Instrument
from utils import resize_img

class Computer(Instrument):
    def __init__(self, x, y):
        super().__init__("computer", x, y)
        self.interface = resize_img(pygame.image.load("assets/images/ui/computer_keys.png"), width=150)

        self.sounds =  {
            "switch": pygame.mixer.Sound("assets/sound/switch.mp3"),
            "reset": pygame.mixer.Sound("assets/sound/reset.mp3"),
            "send": pygame.mixer.Sound("assets/sound/send.mp3")
        }

        self.sounds["switch"].set_volume(2)
        self.sounds["reset"].set_volume(1.5)
        self.sounds["send"].set_volume(1.5)

    def play(self):
        super().play()

    def update(self, now, dt):
        super().update(now, dt)
        
    def draw_interface(self, screen):
        screen.blit(self.interface, (self.rect.x + self.rect.width//2 - self.interface.get_width()//2, self.rect.y-40))
    
    def handle_input(self, key, player, game):
        if key == player.keybinds['right']:
            self.sounds["switch"].play()
            game.selected_track += 1
            if game.selected_track >= len(game.tracks):
                game.selected_track = 0
        elif key == player.keybinds['left']:
            self.sounds["switch"].play()
            game.selected_track -= 1
            if game.selected_track < 0:
                game.selected_track = len(game.tracks) - 1
        elif key == pygame.K_RETURN:
            self.sounds["send"].play()
            if len(game.tracks) and not game.tracks[game.selected_track].sending:
                game.tracks[game.selected_track].send(game.now)
        elif key == pygame.K_r:
            if len(game.tracks) and not game.tracks[game.selected_track].sending:
                game.tracks[game.selected_track].reset()
                self.sounds["reset"].play()