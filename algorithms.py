from config import canvas_width, canvas_height
from Bar import swap, generate_bars
from time import sleep
import config
import pygame
import threading

is_drawing = False
pass_delay = 30
draw_thread = threading.Thread()


def draw_bars(arr, surface):
    bars_changed = []
    bar_group = pygame.sprite.Group()

    for bar in arr:
        if bar.is_changed:
            bars_changed.append(pygame.Rect(bar.rect.x, 0, bar.rect.width, canvas_height))
            bar.is_changed = False

    bar_group.add(arr)

    pygame.draw.rect(surface, (0, 0, 0), pygame.rect.Rect((0, 0), (canvas_width, canvas_height)))
    bar_group.draw(surface)
    pygame.display.update(bars_changed)
    sleep(1 / pass_delay)


def reset_bars(arr, surface):
    bar_group = pygame.sprite.Group()
    bar_group.add(arr)
    pygame.draw.rect(surface, (0, 0, 0), pygame.rect.Rect((0, 0), (canvas_width, canvas_height)))
    bar_group.draw(surface)
    pygame.display.flip()
    sleep(1 / pass_delay)


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
                arr[k] = L[i]
                arr[k].position = start + k
                arr[k].update_position()
                arr[k].passed()

                draw_bars([arr[k]], surface)

                i += 1
                k += 1

            while j < len(R):
                arr[k] = R[j]
                arr[k].position = start + k
                arr[k].update_position()
                arr[k].passed()

                draw_bars([arr[k]], surface)

                j += 1
                k += 1

            [bar.default() for bar in arr]
            draw_bars(arr, surface)

    draw_merge_sort_helper(arr, 0, surface)


def draw_bubble_sort(arr, surface):
    global pass_delay

    swaps = 1
    arr_len = len(arr)
    while swaps != 0:
        swaps = 0
        [bar.default() for bar in arr]
        reset_bars(arr, surface)
        for i in range(arr_len - 1):
            if not is_drawing:
                return

            if arr[i].value > arr[i + 1].value:
                swap(arr[i], arr[i + 1])

                temp = arr[i + 1]
                arr[i + 1] = arr[i]
                arr[i] = temp

                swaps += 1
            else:
                arr[i].passed()
                arr[i + 1].passed()

            draw_bars([arr[i], arr[i + 1]], surface)


def draw_selection_sort(arr, surface):
    global is_drawing

    arr_len = len(arr)
    selected = arr[0]

    for i in range(arr_len):
        [bar.default() for bar in arr if not bar.is_passed]
        reset_bars(arr, surface)
        min_idx = i
        arr[i].pivot()

        for j in range(i + 1, arr_len):
            if not is_drawing:
                return
            if arr[min_idx].value > arr[j].value:
                arr[min_idx].swapped()
                arr[j].selected()
                min_idx = j
                reset_bars(arr, surface)

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
    global is_drawing, pass_delay
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
            draw_bars([array[start]], screen)
            start += 1

        # Decrement the end pointer till it finds an
        # element less than pivot
        while array[end].value > pivot:
            if not is_drawing:
                return
            array[end].passed()
            draw_bars([array[end]], screen)
            end -= 1

        # If start and end have not crossed each other,
        # swap the numbers on start and end
        if start < end:
            swap(array[start], array[end])
            array[start], array[end] = array[end], array[start]
            draw_bars([array[start], array[end]], screen)

    # Swap pivot element with element on end pointer.
    # This puts pivot on its correct sorted place.
    swap(array[end], array[pivot_index])
    array[end], array[pivot_index] = array[pivot_index], array[end]
    array[pivot_index].default()
    array[end].pivot()
    draw_bars([array[end], array[pivot_index]], screen)

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
        reset_bars(array, surface)

        # Sort elements before partition
        # and after partition
        if not is_drawing:
            return
        draw_quick_sort_helper(start, p - 1, array, surface)
        if not is_drawing:
            return
        draw_quick_sort_helper(p + 1, end, array, surface)

        [bar.default() for bar in array]
        reset_bars(array, surface)


def start_draw(algorithm_list, surface, speed_slider, num_values_slider):
    global is_drawing, pass_delay, draw_thread

    if is_drawing:
        return

    is_drawing = True

    algorithm_string = algorithm_list.get_value()

    pass_delay = round(speed_slider.get_value())
    config.num_values = round(num_values_slider.get_value())

    bar_array = generate_bars()
    reset_bars(bar_array, surface)

    if algorithm_string == "Quicksort":
        func = draw_quick_sort
    elif algorithm_string == "Bubble Sort":
        func = draw_bubble_sort
    elif algorithm_string == "Selection Sort":
        func = draw_selection_sort
    elif algorithm_string == "Merge Sort":
        func = draw_merge_sort
    else:
        is_drawing = False
        return

    draw_thread = threading.Thread(target=start_draw_helper, args=(func, bar_array, surface))
    draw_thread.setDaemon(True)
    draw_thread.start()


def start_draw_helper(func, bar_array, surface):
    global is_drawing
    func(bar_array, surface)

    is_drawing = False


def stop_draw():
    global is_drawing
    is_drawing = False


def restart_draw(algorithm_list, surface, speed_slider, num_values_slider):
    global is_drawing, draw_thread
    stop_draw()
    draw_thread.join()
    start_draw(algorithm_list, surface, speed_slider, num_values_slider)
