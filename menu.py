from config import *
from algorithms import start_draw, restart_draw, stop_draw
import sys
import thorpy


def create_menu(screen):
    """
    Places GUI elements of the menu on the given screen and returns the menu object
    :param screen: pygame screen to add menu
    :return: menu object
    """
    speed_slider = thorpy.SliderX(100, (5, 400), "Speed (fps)", initial_value=30)
    num_values_slider = thorpy.SliderX(100, (2, 200), "Bars", initial_value=20)

    algorithm_string_list = ["Quicksort", "Bubble Sort", "Selection Sort", "Merge Sort", "Insertion Sort",
                             "Cocktail Sort"]  # algorithm list
    # algorithm selection
    algorithm_list = thorpy.DropDownListLauncher(const_text="Choose: ", titles=algorithm_string_list)
    algorithm_list.scale_to_title()

    menu_text = thorpy.make_text(text="Menu:")

    params_map = {"algorithm_list": algorithm_list, "surface": screen,
                  "speed_slider": speed_slider,
                  "num_values_slider": num_values_slider}  # parameters to pass to buttons

    start = thorpy.make_button("Start", func=start_draw,  # start button
                               params=params_map)

    stop = thorpy.make_button("Stop", func=stop_draw)  # stop button

    restart = thorpy.make_button("Restart", func=restart_draw, params=params_map)  # restart button

    quit_button = thorpy.make_button("Quit", func=sys.exit, params=0)

    box = thorpy.Box(
        elements=[menu_text, speed_slider, num_values_slider, start, stop, restart, algorithm_list, quit_button])
    box.fit_children(margins=(10, 10))  # we want large margins

    background = thorpy.Background(elements=[box], color=(0, 0, 0))  # set background colour to black
    menu = thorpy.Menu(elements=[background])
    for element in menu.get_population():
        element.surface = screen

    box.set_topleft((canvas_width, 0))
    box.blit()
    box.update()

    return menu
