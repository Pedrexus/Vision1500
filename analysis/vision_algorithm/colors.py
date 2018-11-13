import pandas as pd
from numpy import linalg, array

RED = (255, 0, 0)
COCA_COLA_RED = (177, 43, 44)
ORANGE = (255, 140, 0)
FANTA_ORANGE = (204, 95, 28)
YELLOW = (255, 255, 0)
GREEN = (0, 128, 0)

colors = {
    'red': RED,
    'coca_cola_red': COCA_COLA_RED,
    'orange': ORANGE,
    'fanta_orange': FANTA_ORANGE,
    'yellow': YELLOW,
    'green': GREEN,
}

colors_boundaries = {
    # lists are in BGR, not RGB.
    'coca_cola_red': ([0, 50, 50], [10, 150, 255]),  # [5, 0, 150]
    'red': ([170, 150, 50], [180, 255, 255]),  #
    'orange': ([0, 69, 255], [0, 165, 255]),
    'fanta_orange': ([5, 175, 150], [15, 255, 255]),
    'yellow': ([25, 146, 190], [62, 174, 250]),
    'green': ([50, 205, 154], [170, 178, 32]),
    'blue': ([86, 31, 4], [220, 88, 50]),  #
    'gray': ([103, 86, 65], [145, 133, 128]),  #
}

item = {
    'red': 'coca_cola',
    'coca_cola_red': 'coca_cola',
    'orange': 'fanta',
    'fanta_orange': 'fanta',
    'yellow': 'else',
    'green': 'else',
}


def similar_color_shade(rgb_array):
    # limited to red, orange and rest
    a = array(rgb_array)

    dists = pd.Series(
        {color: linalg.norm(a - array(b)) for color, b in colors.items()})

    return dists.idxmin()


def item_from_rgb(rgb_array):
    return item.get(similar_color_shade(rgb_array), None)
