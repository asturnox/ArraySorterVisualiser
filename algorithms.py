import threading
from time import sleep

import pygame

import config
from Bar import swap, generate_bars

is_drawing = False
draw_thread = threading.Thread()

"""
Contains all sorting algorithms as well as the logic needed to display them.
"""


def start_draw(algorithm_list, surface, speed_slider, num_values_slider):
    """Selects the sorting algorithm to use based on user input and runs it"""
    global is_drawing, pass_delay, draw_thread

    if is_drawing:  # if already drawing, do nothing
        return

    is_drawing = True

    algorithm_string = algorithm_list.get_value()

    pass_delay = round(speed_slider.get_value())
    config.num_values = round(num_values_slider.get_value())

    bar_array = generate_bars()
    clear(surface)
    draw_bars(bar_array, surface)

    if algorithm_string == "Quicksort":
        func = draw_quick_sort
    elif algorithm_string == "Bubble Sort":
        func = draw_bubble_sort
    elif algorithm_string == "Selection Sort":
        func = draw_selection_sort
    elif algorithm_string == "Merge Sort":
        func = draw_merge_sort
    elif algorithm_string == "Insertion Sort":
        func = draw_insertion_sort
    elif algorithm_string == "Cocktail Sort":
        func = draw_cocktail_sort
    else:
        is_drawing = False
        return

    draw_thread = threading.Thread(target=start_draw_helper, args=(func, bar_array, surface))
    draw_thread.setDaemon(True)
    draw_thread.start()


def start_draw_helper(func, bar_array, surface):
    """Helper used to set the is_drawing flag to false when done drawing"""
    global is_drawing
    func(bar_array, surface)

    is_drawing = False


def stop_draw():
    global is_drawing
    is_drawing = False


def restart_draw(algorithm_list, surface, speed_slider, num_values_slider):
    global is_drawing, draw_thread
    stop_draw()
    draw_thread.join()  # wait for drawing to finish at a safe stage
    start_draw(algorithm_list, surface, speed_slider, num_values_slider)


def clear(surface):
    """Clears entire surface to default colour and updates it"""
    rect = pygame.rect.Rect(0, 0, config.canvas_width, config.canvas_height)
    pygame.draw.rect(surface, (0, 0, 0), rect)
    pygame.display.flip()


def draw_bars(arr, surface):
    """Updates bar sections of the surface that have changed.

    Parameters
    ----------
    :param arr: Bar array
    :param surface: surface to draw to
    """
    rectangles_changed = []
    changed_bars = pygame.sprite.Group()

    for bar in arr:
        if bar.is_changed:  # update only sections that have changed
            rect = pygame.Rect(bar.rect.x, 0, bar.rect.width, config.canvas_height)  # take the entire section of the
            # section occupied by the bar

            rectangles_changed.append(rect)  # add to update section of screen
            pygame.draw.rect(surface, (0, 0, 0), rect)  # clear part of screen of rect

            changed_bars.add(bar)  # add sprite to group for drawing
            bar.is_changed = False  # bar will be updated, so is_changed is reset

    changed_bars.draw(surface)  # draw sprites
    pygame.display.update(rectangles_changed)  # update only changed sections
    sleep(1 / pass_delay)  # user delay


# algorithm implementations are found below this point

def draw_merge_sort(arr, surface):
    def draw_merge_sort_helper(arr, start, surface):
        if len(arr) > 1:
            # Finding the mid of the array
            mid = len(arr) // 2

            # Dividing the array elements
            L = arr[:mid]

            # into 2 halves
            R = arr[mid:]

            # Sorting the first half
            draw_merge_sort_helper(L, start + 0, surface)

            # Sorting the second half
            draw_merge_sort_helper(R, start + mid, surface)

            i = j = k = 0

            # Copy data to temp arrays L[] and R[]
            while i < len(L) and j < len(R):
                if not is_drawing:
                    return

                if L[i].value < R[j].value:
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1

                arr[k].position = start + k
                arr[k].update_position()
                arr[k].passed()

                draw_bars([arr[k]], surface)

                k += 1

            # Checking if any element was left
            while i < len(L):
                if not is_drawing:
                    return

                arr[k] = L[i]
                arr[k].position = start + k
                arr[k].update_position()
                arr[k].passed()

                draw_bars(arr, surface)

                i += 1
                k += 1

            while j < len(R):
                if not is_drawing:
                    return

                arr[k] = R[j]
                arr[k].position = start + k
                arr[k].update_position()
                arr[k].passed()

                draw_bars(arr, surface)

                j += 1
                k += 1

            [bar.default() for bar in arr]
            draw_bars(arr, surface)

    draw_merge_sort_helper(arr, 0, surface)


def draw_bubble_sort(arr, surface):
    arr_len = len(arr)
    swapped = True

    while swapped:
        swapped = False
        [bar.default() for bar in arr]  # new pass, set bars to default colour
        draw_bars(arr, surface)
        for i in range(arr_len - 1):
            if not is_drawing:
                return

            if arr[i].value > arr[i + 1].value:
                swap(arr[i], arr[i + 1])

                arr[i], arr[i + 1] = arr[i + 1], arr[i]

                swapped = True
            else:
                arr[i].passed()
                arr[i + 1].passed()

            draw_bars(arr, surface)


def draw_selection_sort(arr, surface):
    arr_len = len(arr)
    selected = arr[0]

    for i in range(arr_len):
        [bar.default() for bar in arr]
        draw_bars(arr, surface)
        min_idx = i
        arr[i].selected()

        for j in range(i + 1, arr_len):
            if not is_drawing:
                return
            if arr[min_idx].value > arr[j].value:
                arr[min_idx].swapped()
                arr[j].selected()
                min_idx = j
                draw_bars(arr, surface)

                if selected.position >= i + 1:
                    selected.swapped()
                arr[min_idx].selected()
                selected = arr[min_idx]
            else:
                arr[j].swapped()

            draw_bars(arr, surface)

        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        swap(arr[i], arr[min_idx])

        arr[i].passed()

        draw_bars(arr, surface)


def partition(start, end, array, screen):
    # Initializing pivot's index to start
    pivot_index = start
    pivot = array[pivot_index].value

    # This loop runs till start pointer crosses
    # end pointer, and when it does we swap the
    # pivot with element on end pointer
    while start < end:

        # Increment the start pointer till it finds an
        # element greater than  pivot
        while start < len(array) and array[start].value <= pivot:
            if not is_drawing:
                return
            array[start].passed()
            draw_bars(array, screen)
            start += 1

        # Decrement the end pointer till it finds an
        # element less than pivot
        while array[end].value > pivot:
            if not is_drawing:
                return
            array[end].passed()
            draw_bars(array, screen)
            end -= 1

        # If start and end have not crossed each other,
        # swap the numbers on start and end
        if start < end:
            swap(array[start], array[end])
            array[start], array[end] = array[end], array[start]
            draw_bars(array, screen)

    # Swap pivot element with element on end pointer.
    # This puts pivot on its correct sorted place.
    swap(array[end], array[pivot_index])
    array[end], array[pivot_index] = array[pivot_index], array[end]
    array[pivot_index].default()
    array[end].pivot()
    draw_bars(array, screen)

    # Returning end pointer to divide the array into 2
    return end


def draw_quick_sort(arr, surface):
    draw_quick_sort_helper(0, len(arr) - 1, arr, surface)


# The main function that implements QuickSort
def draw_quick_sort_helper(start, end, array, surface):
    if start < end:
        # p is partitioning index, array[p]
        # is at right place
        p = partition(start, end, array, surface)
        [bar.default() for bar in array]
        draw_bars(array, surface)

        # Sort elements before partition
        # and after partition
        if not is_drawing:
            return
        draw_quick_sort_helper(start, p - 1, array, surface)
        if not is_drawing:
            return
        draw_quick_sort_helper(p + 1, end, array, surface)

        [bar.default() for bar in array]
        draw_bars(array, surface)


def draw_insertion_sort(arr, surface):
    # Traverse through 1 to len(arr)
    for i in range(1, len(arr)):
        [bar.default() for bar in arr]
        key_value = arr[i].value
        arr[i].passed()

        # Move elements of arr[0..i-1], that are
        # greater than key, to one position ahead
        # of their current position
        j = i - 1

        while j >= 0 and key_value < arr[j].value:
            if not is_drawing:
                return

            arr[j + 1].update_value(arr[j].value)
            arr[j + 1].swapped()
            j -= 1
            draw_bars(arr, surface)

        arr[j + 1].update_value(key_value)
        arr[j + 1].passed()
        draw_bars(arr, surface)
        [bar.default() for bar in arr]
        draw_bars(arr, surface)


def draw_cocktail_sort(a, surface):
    n = len(a)
    swapped = True
    start = 0
    end = n - 1
    while swapped:

        # reset the swapped flag on entering the loop,
        # because it might be true from a previous
        # iteration.
        swapped = False

        # loop from left to right same as the bubble
        # sort
        for i in range(start, end):
            if not is_drawing:
                return

            if a[i].value > a[i + 1].value:
                swap(a[i], a[i + 1])

                a[i], a[i + 1] = a[i + 1], a[i]

                swapped = True
            else:
                a[i].passed()
                a[i + 1].passed()
            draw_bars(a, surface)

        # if nothing moved, then array is sorted.
        if not swapped:
            break

        # otherwise, reset the swapped flag so that it
        # can be used in the next stage
        swapped = False

        # move the end point back by one, because
        # item at the end is in its rightful spot
        end = end - 1

        # from right to left, doing the same
        # comparison as in the previous stage
        for i in range(end - 1, start - 1, -1):
            if not is_drawing:
                return

            if a[i].value > a[i + 1].value:
                swap(a[i], a[i + 1])

                a[i], a[i + 1] = a[i + 1], a[i]

                swapped = True
            else:
                a[i].passed()
                a[i + 1].passed()
            draw_bars(a, surface)

        # increase the starting point, because
        # the last stage would have moved the next
        # smallest number to its rightful spot.
        start = start + 1
        draw_bars(a, surface)
        [bar.default() for bar in a]
        draw_bars(a, surface)
