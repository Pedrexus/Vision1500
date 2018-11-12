import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from google.cloud.vision import types

from analysis.vision_algorithm._activate_api import build_image, client
from .image_properties import localize_objects

STATIC_FONTS = r'C:\Users\Pedro\Documents\PycharmProjects\Vision1500\static\fonts'


def draw_objects_hints(image_path, filename=None, output_format='JPEG',
                       font="OpenSans-Regular.ttf", fontsize=16):
    """Draw a border around the image using the hints in the vector list."""
    objects = localize_objects(image_path)
    if len(objects) == 0:
        raise AttributeError("No objects could be found.")

    im = Image.open(image_path)
    draw = ImageDraw.Draw(im)

    fontsize = int(im.size[0] * fontsize / 200)
    font = ImageFont.truetype(os.path.join(STATIC_FONTS, font), fontsize)
    for name, vertices in objects.items():
        vertices_x = np.array([vertice.x for vertice in vertices]) * im.size[0]
        vertices_y = np.array([vertice.y for vertice in vertices]) * im.size[1]
        vertices_coordinates = list(zip(vertices_x, vertices_y))

        draw.line(
            vertices_coordinates + [vertices_coordinates[0]],
            fill=(250, 250, 250),
            width=5,
            joint='curve',
        )

        draw.text(
            (vertices_x[0] * 1.05, vertices_y[0] * 1.05),
            text=name,
            fill=(250, 250, 250),
            font=font,
        )

    if filename:
        im.save(filename, output_format)
    else:
        im.save('output-draw_hints.jpg', output_format)


def get_crop_hint(path, aspect_ratios=''):
    """Detect crop hints on a single image and return the first result."""

    aspect_ratios = [float(x) for x in aspect_ratios.split(',')]
    crop_hints_params = types.CropHintsParams(aspect_ratios=aspect_ratios)
    image_context = types.ImageContext(crop_hints_params=crop_hints_params)

    response = client.crop_hints(
        image=build_image(path),
        image_context=image_context
    )
    hints = response.crop_hints_annotation.crop_hints

    # Get bounds for the first crop hint using an aspect ratio of 1.77.
    vertices = hints[0].bounding_poly.vertices

    return vertices


def crop_to_hint(image_path, aspect_ratios='1.', filename=None,
                 output_format='JPEG', retimg=False):
    """Crop the image using the hints in the vector list."""
    vects = get_crop_hint(image_path, aspect_ratios)

    im = Image.open(image_path)
    im2 = im.crop([vects[0].x, vects[0].y,
                   vects[2].x - 1, vects[2].y - 1])

    if retimg:
        return im2
    else:
        if filename:
            im2.save(filename, output_format)
        else:
            im2.save('output-draw_hints.jpg', output_format)
