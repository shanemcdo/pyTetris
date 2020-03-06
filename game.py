import pygame
from coord import coord

class game:
    def __init__(self, sz=(300,600)):
        pygame.display.init()
        self.screen = pygame.display.set_mode(size=sz)
        self.running = True

    def play(self):
        #game loop
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screen.fill((0,0,0)) #clear screen
            pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(0, 0, 30, 30))    
            pygame.display.update()