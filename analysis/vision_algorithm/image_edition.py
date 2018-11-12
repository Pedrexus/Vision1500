import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from google.cloud.vision import types

from analysis.vision_algorithm._activate_api import build_image, client
from analysis.vision_algorithm.detect_color import filter_by_color
from .image_properties import localize_objects, detect_prices

STATIC_FONTS_WINDOWS = r'C:\Users\Pedro\Documents\PycharmProjects\Vision1500\static\fonts'
STATIC_FONTS_UBUNTU = r'/home/pedro/PycharmProjects/Vision1500/static/fonts'
try:
    STATIC_FONTS = STATIC_FONTS_UBUNTU
except:
    STATIC_FONTS = STATIC_FONTS_WINDOWS


def draw_hints(image_path, objects, filename=None, output_format='JPEG',
               font="OpenSans-Regular.ttf", fontsize=16, pct=True):
    """Draw a border around the image using the hints in the vector list."""
    if len(objects) == 0:
        raise AttributeError("No objects could be found.")

    im = Image.open(image_path)
    draw = ImageDraw.Draw(im)

    fontsize = int(im.size[0] * fontsize / 200)
    font = ImageFont.truetype(os.path.join(STATIC_FONTS, font), fontsize)
    for name, vertices in objects.items():
        a, b = im.size[0] if pct else 1, im.size[1] if pct else 1
        vertices_x = np.array([vertice.x for vertice in vertices]) * a
        vertices_y = np.array([vertice.y for vertice in vertices]) * b
        vertices_coordinates = list(zip(vertices_x, vertices_y))

        draw.line(
            vertices_coordinates + [vertices_coordinates[0]],
            fill=(5, 5, 5),
            width=5,
            joint='curve',
        )

        draw.text(
            (vertices_x[0] * 1.05, vertices_y[0] * 1.05),
            text=name,
            fill=(5, 5, 5),
            font=font,
        )

    if filename:
        im.save(filename, output_format)
    else:
        im.save('output-draw_hints.jpg', output_format)


def draw_objects_hints(image_path, **kwargs):
    """Draw a border around the image using the hints in the vector list."""
    objects = localize_objects(image_path)
    draw_hints(image_path, objects, **kwargs)


def draw_prices_hints(image_path, min_price=.1, max_price=10., **kwargs):
    """Draw a border around the image using the hints in the vector list."""
    prices = detect_prices(image_path, min_price, max_price)
    draw_hints(image_path, prices, pct=False, **kwargs)


def get_crop_hint(image, aspect_ratios='1.'):
    """Detect crop hints on a single image and return the first result."""

    aspect_ratios = [float(x) for x in aspect_ratios.split(',')]
    crop_hints_params = types.CropHintsParams(aspect_ratios=aspect_ratios)
    image_context = types.ImageContext(crop_hints_params=crop_hints_params)

    response = client.crop_hints(
        image=image,
        image_context=image_context
    )
    hints = response.crop_hints_annotation.crop_hints

    # Get bounds for the first crop hint using an aspect ratio of 1.77.
    crop_hints = {ratio: hint for ratio, hint in zip(aspect_ratios, hints)}

    return crop_hints


def crop_to_hint(source_image, image_to_crop_path, aspect_ratios='1.',
                 filename=None, output_format='JPEG', retimg=False):
    """Crop the image using the hints in the vector list."""
    crop_hints = get_crop_hint(source_image, aspect_ratios)

    """
    best_crop_index = np.argmax(
        [hint.importance_fraction / aspect_ratio for aspect_ratio, hint in
         crop_hints.items()]
    )
    implement for loop in aspect ratios
    """

    crop = list(crop_hints.items())[0][-1]
    vertices = crop.bounding_poly.vertices
    box = (vertices[0].x, vertices[0].y, vertices[2].x, vertices[2].y)
    im2 = Image.open(image_to_crop_path)
    im2 = im2.crop(box)

    if retimg:
        return im2
    else:
        if filename:
            im2.save(filename, output_format)
        else:
            im2.save('output-draw_hints.jpg', output_format)


def crop_by_color(path, color, aspect_ratios='1.', output=None):
    image = build_image(path)  # google vision

    contrast_image = filter_by_color(path, color=color, retimg=True)
    google_cont_img = types.Image(
        content=cv2.imencode('.jpg', contrast_image)[1].tostring()
    )

    crop_to_hint(
        source_image=google_cont_img,
        image_to_crop_path=path, #cv2
        filename=output,
        aspect_ratios=aspect_ratios,
    )
