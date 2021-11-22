from config import *
import pygame
from noise import *
from random import shuffle
import config

padding = 2


class Bar(pygame.sprite.Sprite):

    def __init__(self, value, position):
        super().__init__()
        self.value = value
        self.position = position
        self.image = pygame.surface.Surface(
            (canvas_width / config.num_values - padding, value * canvas_height / config.num_values))
        self.image.fill((255, 255, 255))  # set default colour to white
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.bottomleft = ((canvas_width + padding) / config.num_values * position, canvas_height)
        self.is_passed = False
        self.is_changed = True

    def update_position(self):
        self.rect.bottomleft = ((canvas_width + padding) * self.position / config.num_values, canvas_height)
        self.swapped()

    def update_value(self, value):
        self.value = value
        self.image = pygame.surface.Surface(
            (canvas_width / config.num_values - padding, value * canvas_height / config.num_values))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = ((canvas_width + padding) / config.num_values * self.position, canvas_height)
        self.image.fill((255, 255, 255))

    def swapped(self):
        self.image.fill((255, 0, 0))
        self.is_changed = True

    def default(self):
        self.image.fill((255, 255, 255))
        self.is_passed = False
        self.is_changed = True

    def passed(self):
        self.image.fill((0, 255, 0))
        self.is_passed = True
        self.is_changed = True
        passed_noise(self.value)

    def selected(self):
        self.is_changed = True
        self.image.fill((100, 0, 100))

    def pivot(self):
        self.is_changed = True
        self.image.fill((0, 0, 255))


def generate_bars():
    arr = [i for i in range(config.num_values)]
    shuffle(arr)
    bar_array = [Bar(arr[i] + 1, i) for i in range(config.num_values)]

    return bar_array


def swap(bar1, bar2):
    bar1.position, bar2.position = bar2.position, bar1.position
    bar1.update_position()
    bar2.update_position()
