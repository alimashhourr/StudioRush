import pygame
from player import Player

class Game:
    def __init__(self, width=800, height=600):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.SCREEN_WIDTH = self.screen.get_width()  # Get the width of the fullscreen
        self.SCREEN_HEIGHT = self.screen.get_height()
        pygame.display.set_caption("OverBeat")
        self.GREY = (151,151,151,255)
        
        self.FPS = 60
        self.clock = pygame.time.Clock()

        # Create player object
        self.player = Player(100, 100, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(self.FPS) / 1000  # Get delta time in seconds

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            self.player.update(keys, dt)

            # Appear on screen
            self.screen.fill(self.GREY)
            self.screen.blit(self.player.image, self.player.rect)
            pygame.display.flip()


game = Game()
game.run()
pygame.quit()