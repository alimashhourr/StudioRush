import pygame
from player import Player
from tile import Tile

class Game:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.dt = 0
        self.FPS = 60
        self.running = True

        # Objet joueur
        self.player = Player(400, 500, self.screen.get_width(), self.screen.get_height())

        # Grille de tiles
        self.tile_size = 100
        self.grid = [
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,1,1,1,1,1,1,1,0],
            [0,0,1,0,0,1,0,0,1,0],
            [0,0,1,0,0,1,0,0,1,0],
            [0,0,1,0,0,1,0,0,1,0],
            [0,0,1,0,0,0,0,0,1,0],
            [0,0,1,1,1,1,1,1,1,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0]
        ]

        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x]:
                    self.grid[y][x] = Tile(x, y, self.tile_size)

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
        self.player.update(self.dt, self.grid)

    def display(self):
        self.screen.fill((255, 255, 255))

        # Dessiner la grille
        for line in self.grid:
            for tile in line:
                if tile:
                    tile.draw(self.screen)

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