import pygame


class Button:
    def __init__(self, rect, colour, text=None):
        self.rect = rect
        self.colour = colour
        self.text = text

    def get_state(self, mouse):
        x, y = mouse.get_pos()
        if (
            self.rect[0] <= x <= self.rect[0] + self.rect[2]
            and self.rect[1] <= y <= self.rect[1] + self.rect[3]
        ):
            if mouse.get_pressed()[0]:
                return 2
            return 1
        return 0

    def render(self, win):
        pygame.draw.rect(win, self.colour, self.rect)
        if self.text:
            pass
