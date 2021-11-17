import sys
import pygame
import thorpy
import threading
from config import *
from algorithms import start_draw, stop_draw, restart_draw


def user_check_input_loop(menu):
    def user_check_input():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            menu.react(event)

    while True:
        user_check_input()


def main():
    pygame.init()

    screen = pygame.display.set_mode((canvas_width + side_menu_width, max(canvas_height, side_menu_height)))
    screen.convert()
    pygame.display.set_caption("Array Sorter Visualiser")

    speed_slider = thorpy.SliderX(100, (5, 120), "Speed (fps)", initial_value=30)

    num_values_slider = thorpy.SliderX(100, (2, 200), "Bars", initial_value=20)

    algorithm_string_list = ["Quicksort", "Bubble Sort", "Selection Sort", "Merge Sort"]
    algorithm_list = thorpy.DropDownListLauncher(const_text="Choose: ", titles=algorithm_string_list)
    algorithm_list.scale_to_title()

    menu_text = thorpy.make_text(text="Menu:")

    params_map = {"algorithm_list": algorithm_list, "surface": screen,
                  "speed_slider": speed_slider,
                  "num_values_slider": num_values_slider}

    start = thorpy.make_button("Start", func=start_draw,
                               params=params_map)

    stop = thorpy.make_button("Stop", func=stop_draw)

    restart = thorpy.make_button("Restart", func=restart_draw, params=params_map)

    quit_button = thorpy.make_button("Quit", func=sys.exit, params=0)

    box = thorpy.Box(
        elements=[menu_text, speed_slider, num_values_slider, start, stop, restart, algorithm_list, quit_button])
    box.fit_children(margins=(10, 10))

    background = thorpy.Background(elements=[box], color=(0, 0, 0))
    menu = thorpy.Menu(elements=[background])
    for element in menu.get_population():
        element.surface = screen

    user_thread = threading.Thread(target=user_check_input_loop, args=(menu,))
    user_thread.setDaemon(True)
    user_thread.start()

    box.set_topleft((canvas_width, 0))
    box.blit()
    box.update()

    menu.play()


if __name__ == "__main__":
    main()





