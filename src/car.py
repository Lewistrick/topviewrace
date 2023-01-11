import math
from time import time

import pygame


class Car:
    max_speed = 10
    max_rotspeed = 6

    def __init__(self, x, y, rotation):
        self.x = x
        self.y = y
        self.rotation = rotation
        self.speed = 0
        self.rotspeed = 0
        self.image = pygame.image.load("car.png")
        self.rect = self.image.get_rect()
        self.rect.center = (int(self.x), int(self.y))
        self.start_time = None

    @property
    def pos(self):
        return self.x, self.y

    @property
    def intpos(self):
        return int(self.x), int(self.y)

    def update(self, maxx, maxy):
        # update position
        rot_radians = math.radians(self.rotation)
        self.x += math.cos(rot_radians) * self.speed
        self.y += math.sin(rot_radians) * self.speed

        # update rotation
        self.rotation = (self.rotation + self.rotspeed) % 360

        # keep the car in the screen
        if self.x < 0:
            self.x = 0
            self.speed = 0
        elif self.x > maxx:
            self.x = maxx
            self.speed = 0

        if self.y < 0:
            self.y = 0
            self.speed = 0
        elif self.y > maxy:
            self.y = maxy
            self.speed = 0

        # update the rect
        self.rect.center = (int(self.x), int(self.y))
        return pygame.transform.rotate(self.image, -self.rotation)

    def turn(self, left_pressed: bool, right_pressed: bool):
        self.rotspeed += (right_pressed - left_pressed) * 0.4

        if self.rotspeed > self.max_rotspeed:
            self.rotspeed = self.max_rotspeed
        elif self.rotspeed < -self.max_rotspeed:
            self.rotspeed = -self.max_rotspeed

        if not left_pressed and not right_pressed:
            self.stabilize()

    def stabilize(self):
        """Update rotational speed towards 0 (no left/right was pressed)"""
        if self.rotspeed > 0:
            self.rotspeed = max(0, self.rotspeed - 1)
        elif self.rotspeed < 0:
            self.rotspeed = min(0, self.rotspeed + 1)

    def accelerate(self, up_pressed: bool, down_pressed: bool):
        self.speed += up_pressed - down_pressed

        if self.speed > self.max_speed:
            self.speed = self.max_speed
        elif self.speed < 0:
            self.speed = 0

        if up_pressed and self.start_time is None:
            self.start_time = time()

        if not up_pressed and not down_pressed:
            self.speed = max(0, self.speed - 0.1)

    def slowdown(self):
        """Call this when a slowdown block is touched.

        Gradually slows the car down to max. half the max speed.
        """
        maxspeed = self.max_speed / 2

        if self.speed > maxspeed:
            self.speed -= (self.speed - maxspeed) / 5

    def finish(self):
        """Call this when the finish line is touched.

        Returns the time it took to finish"""
        return time() - self.start_time
