# import the necessary packages
import cv2
import numpy as np

# define the list of boundaries
from analysis.vision_algorithm.colors import colors_boundaries


def filter_by_bgr_boundaries(path_or_image, lower_boundary, upper_boundary,
                             show_img=False, output='output.jpg',
                             retimg=False):
    """Uses OpenCV to filter objects in an image through color.

    Args:
    path_or_image: The path_or_image to the local file.

    taken from: pyimagesearch.com/2014/08/04/opencv-python-color-detection/
    """
    try:
        image = cv2.imread(path_or_image)
    except TypeError:
        image = path_or_image

    lower = np.array(lower_boundary, dtype="uint8")
    upper = np.array(upper_boundary, dtype="uint8")

    # find the colors within the specified boundaries and apply
    # the mask
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_img, lower, upper)

    intersect_img = cv2.bitwise_and(image, image, mask=mask)
    if show_img:
        # show the images
        cv2.imshow("images", np.hstack([image, intersect_img]))
        cv2.waitKey(0)
    if retimg:
        return intersect_img
    else:
        cv2.imwrite(output, mask)


def filter_by_color(path_or_image, color, show_img=False, output='output.jpg',
                    retimg=False):
    lower_boundary, upper_boundary = colors_boundaries[color]

    return filter_by_bgr_boundaries(
        path_or_image,
        lower_boundary,
        upper_boundary,
        show_img,
        output,
        retimg,
    )
