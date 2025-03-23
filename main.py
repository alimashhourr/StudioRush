import pygame
from utils import resize_img
from player import Player
from tile import Tile
from guitar import Guitar

class Game:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.FPS = 60
        self.running = True
        
        # Charger le fond
        self.background = resize_img(pygame.image.load("assets/images/background.png"), width=screen.get_width())

        # Objet joueur
        self.player = Player(400, 500, self.screen.get_width(), self.screen.get_height())
        
        # Guitar
        self.guitar = Guitar(400, 500, 90)

        # Collision
        self.collisions = [
            pygame.Rect(340, 430, 20, 560),
            pygame.Rect(1600, 430, 20, 560),
            pygame.Rect(340, 430, 1280, 20),
            pygame.Rect(340, 955, 1280, 20)
        ]

    def handling_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.player.dir = 'left'
                elif event.key == pygame.K_d:
                    self.player.dir = 'right'

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.vel[1] = -1
        elif keys[pygame.K_s]:
            self.player.vel[1] = 1
        else:
            self.player.vel[1] = 0

        if keys[pygame.K_a]:
            self.player.vel[0] = -1
        elif keys[pygame.K_d]:
            self.player.vel[0] = 1
        else:
            self.player.vel[0] = 0

    def update(self):
        now = pygame.time.get_ticks()
        self.player.update(self.dt, self.collisions)
        print(self.player.hitbox.topleft)

    def display(self):
        # Dessiner l'image de fond
        self.screen.blit(self.background, (0, 0))

        self.player.draw(self.screen)

        # for rect in self.collisions:
        #     pygame.draw.rect(self.screen, (255, 0, 0), rect)

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