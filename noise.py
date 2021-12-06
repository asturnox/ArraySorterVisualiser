import winsound

from config import num_values

"""Contains all logic to produce sound when passes have been completed."""


def passed_noise(value):
    # TODO: Use a more optimised library
    #  TODO: Create own frequencies from base audio file and play them.
    winsound.Beep(round(2000 + min(30000 * value / num_values, 30000)), 1)
