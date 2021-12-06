from random import shuffle

import pygame

import config
from config import *
from noise import *

padding = 2


class Bar(pygame.sprite.Sprite):
    """Represents a bar/rectangle with a given height, position and color when sorting."""

    def __init__(self, value, position):
        """
        :param value: height of bar
        :param position: position of bar relative to other bars (in main bar array)
        """
        super().__init__()
        self.value = value
        self.position = position
        self.image = pygame.surface.Surface(
            (canvas_width / config.num_values - padding, value * canvas_height / config.num_values))
        self.image.fill((255, 255, 255))  # set default colour to white
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.bottomleft = ((canvas_width + padding) / config.num_values * position, canvas_height)
        self.is_changed = True

    def update_position(self):
        """
        Resets rectangle coordinates to match current position in array
        """
        self.rect.bottomleft = ((canvas_width + padding) * self.position / config.num_values, canvas_height)
        self.swapped()

    def update_value(self, value):
        """
        Changes value according to parameter, updates position of rectangle subsequently
        :param value: height to change value
        """
        self.value = value
        self.image = pygame.surface.Surface(
            (canvas_width / config.num_values - padding, value * canvas_height / config.num_values))
        self.rect = self.image.get_rect()
        self.rect.bottomleft = ((canvas_width + padding) / config.num_values * self.position, canvas_height)
        self.image.fill((255, 255, 255))

    def swapped(self):
        """
        Indicates that the Bar has been swapped.
        Changes Bar color to red and indicates that Bar has changed.
        """
        self.image.fill((255, 0, 0))
        self.is_changed = True

    def default(self):
        """
        Indicates that the Bar has been normalised. This usually happens when a sorting phase is done.
        Sets the Bar's color to white.
        Indicates that Bar has changed.
        """
        self.image.fill((255, 255, 255))
        self.is_changed = True

    def passed(self):
        """
        Indicates that the Bar has been passed when sorting. Usually happens when no swapping is need.
        Sets the Bar's color to green.
        Indicates the Bar has changed.
        """
        self.image.fill((0, 255, 0))
        self.is_changed = True
        passed_noise(self.value)

    def selected(self):
        """
        Indicates that the Bar has been selected as a particular value, such as the minimum current (selection sort).
        Sets the Bar's color to purple.
        Indicates the Bar has changed.
        """
        self.is_changed = True
        self.image.fill((100, 0, 100))

    def pivot(self):
        """
        Indicates that the Bar has been selected as a pivot, such as in quick sort.
        Sets the Bar's color to blue.
        Indicates the Bar has changed.
        """
        self.is_changed = True
        self.image.fill((0, 0, 255))


def generate_bars():
    """
    Generates an array of shuffled Bar objects with distinct heights and returns it.
    :return: shuffled array of Bar objects
    """
    arr = [i for i in range(config.num_values)]
    shuffle(arr)
    bar_array = [Bar(arr[i] + 1, i) for i in range(config.num_values)]

    return bar_array


def swap(bar1, bar2):
    """Swaps two given bar objects and updates their rectangles"""
    bar1.position, bar2.position = bar2.position, bar1.position
    bar1.update_position()
    bar2.update_position()
