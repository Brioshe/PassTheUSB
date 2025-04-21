import pygame

class Game():
    def __init__(self):
        pygame.init()
        infoObject = pygame.display.Info() # Display info object (for width and height mostly)

        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = infoObject.current_w, infoObject.current_h
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        self.fontText = pygame.font.SysFont('Segoe UI', 30)
        pass