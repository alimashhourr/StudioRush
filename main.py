import pygame
from player import Player

class Game:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.FPS = 60
        self.running = True

        # Objet joueur
        self.player = Player(100, 100, self.screen.get_width(), self.screen.get_height())

    def handling_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.player.dir = 'left'
                elif event.key == pygame.K_d:
                    self.player.dir = 'right'

    def update(self):
        now = pygame.time.get_ticks()
        self.player.update(pygame.key.get_pressed(), self.dt)

    def display(self):
        self.screen.fill((255, 255, 255))
        self.player.draw(self.screen)

        # Mettre à jour l'écran
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handling_events()
            self.update()
            self.display()
            self.dt = self.clock.tick(self.FPS) / 1000

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Studio Rush")

game = Game(screen)
game.run()

pygame.quit()