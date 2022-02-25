import sys
import threading

import pygame
from config import *
from menu import create_menu


def user_check_input_loop(menu):
    """Continually checks for user input on a separate thread, reacts accordingly"""

    def user_check_input():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            menu.react(event)

    while True:
        user_check_input()  # always check for user interaction


def main():
    """
    Main application loop, initialises and places GUI elements
    """
    pygame.init()

    # create screen
    screen = pygame.display.set_mode((canvas_width + side_menu_width, max(canvas_height, side_menu_height)))
    # convert screen for successive drawing
    screen.convert()

    pygame.display.set_caption("Array Sorter Visualiser")

    # add menu to screen
    menu = create_menu(screen)
    # start menu
    menu.play()

    # check if user interacts with menu
    user_thread = threading.Thread(target=user_check_input_loop, args=(menu,))
    user_thread.setDaemon(True)
    user_thread.start()


if __name__ == "__main__":
    main()
