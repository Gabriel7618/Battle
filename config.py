from MOD import *
import os
import pygame
import time

pygame.init()

WIDTH, HEIGHT = 1300, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battle!")

CLOCK = pygame.time.Clock()
FPS = 40

title_font = pygame.font.SysFont("impact", 100)
title_text = "Battle!"
title_rendered_text = title_font.render(title_text, True, "white", "black")

countdown_font = pygame.font.SysFont("arial", 50, True)
countdown_words = ("3", "2", "1")

start_button = Button(
    (WIDTH / 2, 0.65 * HEIGHT), (255, 100, 0), "Start", (0, 0, 0), "arial", 50
)

side_block_y = HEIGHT / 2
side_block_width = 0.15 * WIDTH
central_block_width = WIDTH - 2 * side_block_width
blockT = Block(
    (side_block_width, 0.25 * HEIGHT, central_block_width, HEIGHT / 50), (255, 255, 255)
)
blockL = Block((0, side_block_y, side_block_width, HEIGHT / 50), (0, 0, 255))
blockR = Block(
    (WIDTH - side_block_width, side_block_y, side_block_width, HEIGHT / 50), (255, 0, 0)
)
blockB = Block(
    (side_block_width, 0.75 * HEIGHT, central_block_width, HEIGHT / 50), (255, 255, 255)
)
lava = Block((0, 0.85 * HEIGHT, WIDTH, 0.2 * HEIGHT), (255, 100, 0), 20)

player_width, player_height = 50, 100
player_y = side_block_y - player_height
laserlady = Player(
    (
        side_block_width / 2 - player_width / 2,
        player_y,
        player_width,
        player_height,
    ),
    False,
    0.5,
    1.3e6,
    100,
    "LaserLady",
    4.5e4,
    2000,
    3000,
)
axeman = Player(
    (
        WIDTH - side_block_width / 2 - player_width / 2,
        player_y,
        player_width,
        player_height,
    ),
    True,
    0.75,
    1.4e6,
    150,
    "Axeman",
    4.6e4,
    2000,
    3000,
    "Axe",
)


def reset(player1, player2, width, side_block_width):
    player_width, player_height = 50, 100
    player_y = side_block_y - player_height

    player1.x = side_block_width / 2 - player_width / 2
    player1.y = player_y
    player1.w = player_width
    player1.h = player_height
    player1.is_left = False

    player2.x = width - side_block_width / 2 - player_width / 2
    player2.y = player_y
    player2.w = player_width
    player2.h = player_height
    player2.is_left = True
    player2.hitbox = [player2.x - 30, player2.y + 4, 75, 75]

    for player in (player1, player2):
        player.disps = [0, 0]
        player.vels = [0, 0]
        player.walk_count = 0
        player.is_attack = False
        player.attack_count = 0
        player.is_cooldown = False
        player.attack_timer_set = False
        player.health = player.max_health
