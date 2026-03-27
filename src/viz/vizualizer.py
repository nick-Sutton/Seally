from typing import Tuple

import pygame
from env.enviroment import Enviroment


class Visualizer2D:
    def __init__(self, screen_size: Tuple[float, float] = (1280, 720)):
        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        self.clock = pygame.time.Clock()
        self.running = False

    def run_visualization(self, path, env: Enviroment):
        self.running = True

        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill("purple")

            # RENDER YOUR GAME HERE

            # flip() the display to put your work on screen
            pygame.display.flip()

            self.clock.tick(60)  # limits FPS to 60

        pygame.quit()