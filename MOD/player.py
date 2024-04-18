from .utils import contains, ontop
import math
import os
import pygame
import time

pygame.init()


class Player:
    players = []
    laser_sound = pygame.mixer.Sound(os.path.join("SFX", "Laser.wav"))
    jump_sound = pygame.mixer.Sound(os.path.join("SFX", "Jump.wav"))
    jump_sound.set_volume(0.45)

    def __init__(
        self,
        rect,
        is_left,
        walk_disp,
        jump_vel,
        initial_health,
        img,
        dps,
        attack_duration,
        cooldown_duration,
        weapon_img=None,
    ):
        self.x, self.y, self.w, self.h = rect
        self.is_left = is_left
        self.walk_disp = walk_disp
        self.disps = [0, 0]
        self.vels = [0, 0]
        self.accels = [0, 4e9]
        self.walk_count = 0
        self.jump_vel = jump_vel
        self.max_health = initial_health
        self.health = initial_health
        self.img = img

        self.is_attack = False
        self.attack_count = 0
        self.is_cooldown = False
        self.dps = dps
        self.attack_timer_set = False
        self.attack_duration = attack_duration
        self.cooldown_duration = cooldown_duration
        if self.img == "LaserLady":
            self.hitbox = None
        elif self.is_left:
            self.hitbox = [self.x - 30, self.y + 4, 75, 75]
        else:
            self.hitbox = [self.x - 8, self.y + 4, 75, 75]
        self.initial_axe_vel = 4e2
        self.axe_vel = self.initial_axe_vel
        self.axe_accel = self.axe_vel * 1000 / (self.attack_duration * 0.9)
        self.axe_left = None
        self.weapon_img = weapon_img

        Player.players.append(self)

    def __move(self, delta_time, blocks, width, height):
        delta_time /= 1000
        disps = [self.disps[i] + vel * delta_time for i, vel in enumerate(self.vels)]
        for i, accel in enumerate(self.accels):
            self.vels[i] += accel * delta_time

        if disps[0]:
            self.x += disps[0]
            self.disps[0] = 0
            for block in blocks:
                if contains(
                    (self.x, self.y, self.w, self.h),
                    (block.x, block.y, block.w, block.h),
                ):
                    if disps[0] > 0:
                        self.x = block.x - self.w
                    elif disps[0] < 0:
                        self.x = block.x + block.w
                    self.vels[0] = 0
                elif self.x < 0:
                    self.x = 0
                elif self.x + self.w > width:
                    self.x = width - self.w

        if disps[1]:
            self.y += disps[1]
            self.disps[1] = 0
            for block in blocks:
                if contains(
                    (self.x, self.y, self.w, self.h),
                    (block.x, block.y, block.w, block.h),
                ):
                    if disps[1] > 0:
                        self.y = block.y - self.h
                    elif disps[1] < 0:
                        self.y = block.y + block.h
                    self.vels[1] = 0
                elif self.y < 0:
                    self.y = 0
                    self.vels[1] = 0
                elif self.y + self.h > height:
                    self.y = height - self.h

    def walk(self, walk_left):
        self.walk_count += 1
        if walk_left:
            self.is_left = True
            self.disps[0] -= self.walk_disp
        else:
            self.is_left = False
            self.disps[0] += self.walk_disp

    def jump(self, blocks):
        for block in blocks[:4]:
            if ontop(
                (self.x, self.y, self.w, self.h), (block.x, block.y, block.w, block.h)
            ):
                self.vels[1] = -self.jump_vel
                self.jump_sound.play()

    def attack(self):
        if not self.is_cooldown:
            self.is_attack = True

    def __attack(
        self,
        target,
        attack_end_event,
        cooldown_end_event,
        ignore_events,
        delta_time,
        width,
    ):
        for event in pygame.event.get(None, True, ignore_events):
            if event.type == attack_end_event:
                self.is_attack = False
                self.attack_count = 0
                self.attack_timer_set = False
                if self.img == "LaserLady":
                    self.hitbox = None
                else:
                    self.axe_vel = self.initial_axe_vel
                    self.axe_left = None
                pygame.time.set_timer(cooldown_end_event, self.cooldown_duration, 1)
                self.is_cooldown = True
            elif event.type == cooldown_end_event:
                self.is_cooldown = False

        if self.is_attack:
            if not self.attack_timer_set:
                pygame.time.set_timer(attack_end_event, self.attack_duration, 1)
                self.attack_timer_set = True

                if self.img == "LaserLady":
                    self.laser_sound.play()

            if self.img == "Axeman":
                axeman_attack(self, target, delta_time)
            elif self.img == "LaserLady":
                laserlady_attack(self, target, delta_time, width)
        elif self.img == "Axeman":
            if self.is_left:
                self.hitbox = [self.x - 30, self.y + 4, 75, 75]
            else:
                self.hitbox = [self.x - 8, self.y + 4, 75, 75]

    def __lava(self, lava):
        if ontop((self.x, self.y, self.w, self.h), (lava.x, lava.y, lava.w, lava.h)):
            self.vels[1] = -1e6
            self.health -= lava.dph
            lava.splash_sound.play()

    def loop(
        self,
        previous_time,
        blocks,
        width,
        height,
        target,
        attack_end_event,
        cooldown_end_event,
        ignore_events,
    ):
        delta_time = time.time() - previous_time
        self.__lava(blocks[4])
        self.__move(delta_time, blocks, width, height)
        self.__attack(
            target,
            attack_end_event,
            cooldown_end_event,
            ignore_events,
            delta_time,
            width,
        )

    def render(self, win):
        x = int(round(self.x))
        y = int(round(self.y))

        period = int(30 / self.walk_disp)
        img = self.walk_count % (9 * period) // period
        if img == 5:
            img = 3
        elif img == 6:
            img = 2
        elif img == 7:
            img = 1
        elif img == 8:
            img = 0
        img = str(img) + ".gif"

        if self.is_left:
            win.blit(
                pygame.image.load(os.path.join("IMG", "Players", self.img, img)),
                (x, y),
            )
        else:
            win.blit(
                pygame.transform.flip(
                    pygame.image.load(os.path.join("IMG", "Players", self.img, img)),
                    True,
                    False,
                ),
                (x, y),
            )

        fade = pygame.Surface((self.w + 60, 10))
        fade.fill((255, 0, 0))
        fade.set_alpha(130)
        win.blit(fade, (x - 30, y - 40))
        if self.health > 0:
            pygame.draw.rect(
                win,
                (0, 255, 0),
                (
                    x - 30,
                    y - 40,
                    int((self.w + 60) * self.health / self.max_health),
                    10,
                ),
            )

        # Render Weapon
        if self.img == "Axeman":
            period = 12
            rot = str(self.attack_count % (4 * period) // period) + ".gif"
            if self.is_left:
                win.blit(
                    pygame.transform.flip(
                        pygame.image.load(
                            os.path.join("IMG", "Weapons", self.weapon_img, rot)
                        ),
                        True,
                        False,
                    ),
                    self.hitbox[:2],
                )
            else:
                win.blit(
                    pygame.image.load(
                        os.path.join("IMG", "Weapons", self.weapon_img, rot)
                    ),
                    self.hitbox[:2],
                )

        elif self.img == "LaserLady":
            if self.is_attack:
                pygame.draw.rect(win, (255, 255, 25), self.hitbox)


def axeman_attack(axeman, target, delta_time):
    axeman.attack_count += 1

    if axeman.axe_vel < 0:
        return_axe(axeman, target, delta_time)
    else:
        axeman.axe_vel -= axeman.axe_accel * delta_time

        if axeman.axe_left == None:
            axeman.axe_left = axeman.is_left
        if axeman.axe_left:
            axeman.hitbox[0] -= axeman.axe_vel * delta_time
        else:
            axeman.hitbox[0] += axeman.axe_vel * delta_time

    if contains(axeman.hitbox, (target.x, target.y, target.w, target.h)):
        target.health -= axeman.dps * delta_time / 1000


def return_axe(axeman, target, delta_time):
    x = abs(axeman.x - axeman.hitbox[0])
    y = abs(axeman.y - axeman.hitbox[1])
    theta = math.atan(y / x)
    vel = 5e3

    if axeman.x > axeman.hitbox[0]:
        axeman.hitbox[0] += vel * math.cos(theta) * delta_time
    else:
        axeman.hitbox[0] -= vel * math.cos(theta) * delta_time

    if axeman.y > axeman.hitbox[1]:
        axeman.hitbox[1] += vel * math.sin(theta) * delta_time
    else:
        axeman.hitbox[1] -= vel * math.sin(theta) * delta_time


def laserlady_attack(laserlady, target, delta_time, width):
    if not laserlady.hitbox:
        if laserlady.is_left:
            laserlady.hitbox = (
                0,
                int(laserlady.y) + laserlady.h - 60,
                laserlady.x,
                7,
            )
        else:
            laserlady.hitbox = (
                laserlady.x + laserlady.w,
                int(laserlady.y) + laserlady.h - 60,
                width,
                7,
            )

    if contains(laserlady.hitbox, (target.x, target.y, target.w, target.h)):
        target.health -= laserlady.dps * delta_time / 1000
