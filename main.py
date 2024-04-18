from MOD import *
from config import *
import pygame
import time

pygame.init()


def main():  # AxeSound & Display who won
    start = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        if (
            start_button.get_state(
                pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0]
            )
            == 2
        ):
            start = True
        elif start:
            reset(laserlady, axeman, WIDTH, side_block_width)
            transition_fade(
                WIN, 175, 0, 1, render_game_window, Player.players, Block.blocks
            )
            if not play_game():
                return
            start = False

        render_game_window(WIN, Player.players, Block.blocks)
        render_menu(WIN, title_rendered_text, start_button)
        pygame.display.update()


def play_game():
    previous_time = time.time()
    laser_attack_end_event = pygame.USEREVENT
    laser_cooldown_end_event = pygame.USEREVENT + 1
    axe_attack_end_event = pygame.USEREVENT + 2
    axe_cooldown_end_event = pygame.USEREVENT + 3
    countdown_end_event = pygame.USEREVENT + 4

    for word in countdown_words:
        render_game_window(WIN, Player.players, Block.blocks)
        countdown_rendered = countdown_font.render(word, True, "white")
        countdown_w, countdown_h = countdown_rendered.get_size()
        WIN.blit(
            countdown_rendered,
            (WIDTH / 2 - countdown_w / 2, HEIGHT / 2 - countdown_h / 2),
        )
        pygame.display.update()
        pygame.time.delay(1000)
    battle_rendered = countdown_font.render("Battle!", True, "white")
    battle_text_w, battle_text_h = battle_rendered.get_size()
    render_battle_text = True
    pygame.time.set_timer(countdown_end_event, 2000, 1)

    while True:
        for event in pygame.event.get(
            None,
            True,
            (
                laser_attack_end_event,
                laser_cooldown_end_event,
                axe_attack_end_event,
                axe_cooldown_end_event,
            ),
        ):
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            elif event.type == countdown_end_event:
                render_battle_text = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            laserlady.walk(True)
        elif keys[pygame.K_d]:
            laserlady.walk(False)

        if keys[pygame.K_LEFT]:
            axeman.walk(True)
        elif keys[pygame.K_RIGHT]:
            axeman.walk(False)

        if keys[pygame.K_w]:
            laserlady.jump(Block.blocks)

        if keys[pygame.K_UP]:
            axeman.jump(Block.blocks)

        if not render_battle_text and keys[pygame.K_SPACE]:
            laserlady.attack()

        if not render_battle_text and keys[pygame.K_RETURN]:
            axeman.attack()

        laserlady.loop(
            previous_time,
            Block.blocks,
            WIDTH,
            HEIGHT,
            axeman,
            laser_attack_end_event,
            laser_cooldown_end_event,
            (axe_attack_end_event, axe_cooldown_end_event, pygame.QUIT),
        )
        axeman.loop(
            previous_time,
            Block.blocks,
            WIDTH,
            HEIGHT,
            laserlady,
            axe_attack_end_event,
            axe_cooldown_end_event,
            (laser_attack_end_event, laser_cooldown_end_event, pygame.QUIT),
        )
        previous_time = time.time()

        for player in Player.players:
            if player.health <= 0:
                return True

        render_game_window(WIN, Player.players, Block.blocks)
        if render_battle_text:
            WIN.blit(
                battle_rendered,
                (WIDTH / 2 - battle_text_w / 2, HEIGHT / 2 - battle_text_h / 2),
            )
        pygame.display.update()


if __name__ == "__main__":
    main()
