import pygame

class MainMenu ():
    def __init__(self):
        self.menu = pygame.image.load("assets/images/ui/main_menu.png")

        self.button_positions = [
            (88, 491),   # Button 1
            (88, 713),   # Button 2
            (1375, 491), # Button 3
            (1375, 713), # Button 4
            (732, 517)    # Button 5 (play)
        ]

        self.players = 1
        self.game_type = 0

        self.buttons = []
        for i in range(1, 6):
            button = {}
            button["normal_img"] = pygame.image.load(f"assets/images/ui/Button_{i}.png")
            button["picked_img"] = pygame.image.load(f"assets/images/ui/Button_{i}_picked.png")
            button["rect"] = button["normal_img"].get_rect(x=self.button_positions[i-1][0], y=self.button_positions[i-1][1])
            self.buttons.append(button)
        
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for i, button in enumerate(self.buttons):
            self.buttons_active[i]
            button["active"] = button["rect"].collidepoint(mouse_pos)

    def draw_menu(self,screen):
        screen.blit(self.menu, (0, 0))
        for i, button in enumerate(self.buttons):
            if i == 0 and self.players == 1 or i == 2 :
                screen.blit(button["picked_img"], button["rect"])
            else:
                screen.blit(button["normal_img"], button["rect"])