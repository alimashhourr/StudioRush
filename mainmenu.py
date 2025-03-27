import pygame

class MainMenu ():
    def __init__(self):
        self.menu = pygame.image.load("assets/images/ui/main_menu.png")
        
        self.players = 1
        self.game_type = 1
        
        button_positions = {
            "1p": (88, 491),   # 1p
            "2p": (88, 713),   # 2p
            "rapide": (1375, 491), # rapide
            "normale": (1375, 713), # normale
            "play": (732, 517)   # play
        }
        
        self.buttons = []
        for name in button_positions.keys():
            button = {}
            button["name"] = name
            button["img"] = pygame.image.load(f"assets/images/ui/button_{name}.png")
            button["img_hover"] = button["img"].copy()
            button["img_hover"].fill((100, 100, 100, 50), special_flags=pygame.BLEND_RGBA_ADD)
            if name != "play":
                button["selected_img"] = pygame.image.load(f"assets/images/ui/button_{name}_selected.png")
                button["selected_img_hover"] = button["selected_img"].copy()
                button["selected_img_hover"].fill((100, 100, 100, 50), special_flags=pygame.BLEND_RGBA_ADD)
            button["rect"] = button["img"].get_rect(x=button_positions[name][0], y=button_positions[name][1])
            self.buttons.append(button)
            
        self.sound = pygame.mixer.Sound("assets/sound/click.mp3")
        self.sound.set_volume(0.5)
        
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for i, button in enumerate(self.buttons):
            #button["rect"].collidepoint(mouse_pos)
            pass
    
    def click(self):
        for button in self.buttons:
            if button["rect"].collidepoint(pygame.mouse.get_pos()):
                if button["name"] in ["1p", "2p", "rapide", "normale"]:
                    self.sound.play()
                    if button["name"] == "1p":
                        self.players = 1
                    elif button["name"] == "2p":
                        self.players = 2
                    elif button["name"] == "rapide":
                        self.game_type = 1
                    elif button["name"] == "normale":
                        self.game_type = 2
                    break
                if button["name"] == "play":
                    self.sound.play()
                    return True
        return False

    def draw_menu(self,screen):
        screen.blit(self.menu, (0, 0))
        for button in self.buttons:
            if button["rect"].collidepoint(pygame.mouse.get_pos()):
                hover = "_hover"
            else:
                hover = ""
            name = button["name"]
            if (name == "1p" and self.players == 1) or (name == "2p" and self.players == 2) or (name == "rapide" and self.game_type == 1) or (name == "normale" and self.game_type == 2):
                screen.blit(button[f"selected_img{hover}"], button["rect"])
            else:
                screen.blit(button[f"img{hover}"], button["rect"])