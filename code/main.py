import pygame
from chef import Chef

class Game:
    def __init__(self, width=800, height=600):
        pygame.init()
        # Screen dimensions
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.SCREEN_WIDTH = self.screen.get_width()  # Get the width of the fullscreen
        self.SCREEN_HEIGHT = self.screen.get_height()
        pygame.display.set_caption("OverBeat")
        self.GREY = (151,151,151,255)
        
        self.FPS = 60
        self.clock = pygame.time.Clock()

        self.idle_animation = [pygame.image.load(f"idle_{i}.png") for i in range(1, 5)]  # 4 idle frames
        self.run_animations = {
            "up": [pygame.image.load(f"run_up_{i}.png") for i in range(1, 5)],  # 4 running frames (up)
            "down": [pygame.image.load(f"run_down_{i}.png") for i in range(1, 5)],  # 4 running frames (down)
            "left": [pygame.image.load(f"run_left_{i}.png") for i in range(1, 5)],  # 4 running frames (left)
            "right": [pygame.image.load(f"run_right_{i}.png") for i in range(1, 5)],  # 4 running frames (right)
        }

        # Create chef object
        self.chef = Chef(self.idle_animation, self.run_animations, 100, 100, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(self.FPS) / 1000  # Get delta time in seconds

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update chef
            keys = pygame.key.get_pressed()
            self.chef.update(keys, dt)

            # Draw everything
            self.screen.fill(self.GREY)
            self.screen.blit(self.chef.image, self.chef.rect)
            pygame.display.flip()

# Main script
if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()