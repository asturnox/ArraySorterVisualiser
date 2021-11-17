from config import num_values
import winsound


def passed_noise(value):
    winsound.Beep(round(2000 + min(30000 * value / num_values, 30000)), 1)
