import os
import pygame

pygame.init()


class Block:
    blocks = []
    splash_sound = pygame.mixer.Sound(os.path.join("SFX", "Splash.wav"))
    splash_sound.set_volume(0.35)

    def __init__(self, rect, colour, dph=None):
        self.x, self.y, self.w, self.h = rect
        self.colour = colour
        self.dph = dph
        Block.blocks.append(self)

    def render(self, win):
        pygame.draw.rect(
            win, self.colour, (int(self.x), int(self.y), int(self.w), int(self.h))
        )
