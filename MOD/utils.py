import pygame


class Button:
    def __init__(
        self,
        centre,
        colour,
        text,
        text_colour,
        font_name,
        font_size,
    ):
        self.centre = centre
        self.colour = colour
        self.text = text
        self.text_colour = text_colour
        self.font_name = font_name
        self.font_size = font_size
        self.offset_x = 10
        self.offset_y = 5

    def get_rect(self, scalar=1):
        font = pygame.font.SysFont(self.font_name, int(self.font_size * scalar))
        text_w, text_h = font.size(self.text)
        offset_x = int(self.offset_x * scalar)
        offset_y = int(self.offset_y * scalar)

        return (
            self.centre[0] - text_w / 2 - offset_x,
            self.centre[1] - text_h / 2 - offset_y,
            text_w + 2 * offset_x,
            text_h + 2 * offset_y,
        )

    def get_state(self, mouse_pos, mouse_pressed):
        if contains(self.get_rect(), (*mouse_pos, 0, 0)):
            if mouse_pressed:
                return 2
            return 1
        return 0

    def render(self, win, button_state):
        if button_state != 0:
            colour = tuple([max(colour_comp - 50, 0) for colour_comp in self.colour])
            if button_state == 2:
                scalar = 0.85
                font_size = int(scalar * self.font_size)
            else:
                scalar = 1
        else:
            colour = self.colour
            scalar = 1

        font = pygame.font.SysFont(self.font_name, int(self.font_size * scalar))
        rendered_text = font.render(self.text, True, self.text_colour)
        rendered_text_w, rendered_text_h = rendered_text.get_size()

        pygame.draw.rect(win, colour, self.get_rect(scalar))
        win.blit(
            rendered_text,
            (
                self.centre[0] - rendered_text_w / 2,
                self.centre[1] - rendered_text_h / 2,
            ),
        )


def render_game_window(win, players, blocks):
    win.fill((0, 0, 0))
    for block in blocks:
        block.render(win)
    for player in players:
        player.render(win)


def render_menu(win, title_rendered_text, start_button):
    fade_screen(win, 175)
    win.blit(
        title_rendered_text,
        (
            win.get_size()[0] / 2 - title_rendered_text.get_size()[0] / 2,
            0.3 * win.get_size()[1] - title_rendered_text.get_size()[1] / 2,
        ),
    )
    start_button.render(
        win,
        start_button.get_state(pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0]),
    )


def contains(rect1, rect2):
    if (
        rect1[0] < rect2[0] + rect2[2] < rect1[0] + rect1[2] + rect2[2]
        and rect1[1] < rect2[1] + rect2[3] < rect1[1] + rect1[3] + rect2[3]
    ):
        return True
    return False


def ontop(rect1, rect2):
    if (
        rect1[0] < rect2[0] + rect2[2] < rect1[0] + rect1[2] + rect2[2]
        and rect1[1] + rect1[3] == rect2[1]
    ):
        return True
    return False


def fade_screen(win, alpha):
    faded_screen = pygame.Surface(win.get_size())
    faded_screen.fill((0, 0, 0))
    faded_screen.set_alpha(alpha)
    win.blit(faded_screen, (0, 0))


def transition_fade(win, alpha_start, alpha_end, duration, render, *render_args):
    if alpha_start < alpha_end:
        alphas = range(alpha_start + 1, alpha_end + 1)
    else:
        alphas = list(range(alpha_end, alpha_start))[::-1]

    delay = duration * 1000 / len(alphas)
    for alpha in alphas:
        render(win, *render_args)
        fade_screen(win, alpha)
        pygame.display.update()
        pygame.time.delay(duration)
