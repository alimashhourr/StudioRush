import pygame
import math
from font import Font
from utils import resize_img

class UserInterface:
    def __init__(self):
        self.font = Font('assets/images/font', 70)
        self.score_icon = resize_img(pygame.image.load("assets/images/ui/score_icon.png"), height=60)
        self.clock_icon = resize_img(pygame.image.load("assets/images/ui/clock.png"), height=60)
        self.gameover_window = pygame.image.load("assets/images/ui/game_over.png")
        
    def draw(self, screen, score, timer, gameover, clients):
        pygame.draw.rect(screen, (255, 255, 255), (0, 1080-75, 300, 75))
        screen.blit(self.score_icon, (10, 1010))
        self.font.display(screen, str(score), 90, 1080-70, 2)
        
        pygame.draw.rect(screen, (255, 255, 255), (1920-330, 1080-75, 330, 75))
        screen.blit(self.clock_icon, (1920-320, 1010))
        minutes = math.floor(timer // 60)
        seconds = math.floor(timer % 60)
        self.font.display(screen, f"{minutes:02}:{seconds:02}", 1680, 1080-70, 2)
        
        if gameover:
            screen.blit(self.gameover_window, (1920/2 - self.gameover_window.get_width()//2, 1080/2 - self.gameover_window.get_height()//2))
            self.font.display(screen, str(score), 850, 524, 2)
            self.font.display(screen, str(clients), 945, 666, 2)