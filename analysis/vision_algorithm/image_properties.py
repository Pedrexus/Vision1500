import base64
from collections import defaultdict
from io import BytesIO

from PIL import Image
from google.cloud.vision import types

from ._activate_api import build_image, client
from .colors import item_from_rgb


def detect_areas(path):
    """Detects image properties in the file."""
    response = client.image_properties(image=build_image(path))
    props = response.image_properties_annotation

    items_areas = defaultdict(list)
    total_area = 0
    for color in props.dominant_colors.colors:
        rgb = color.color
        item = item_from_rgb(
            (rgb.red, rgb.green, rgb.blue)
        )

        area = color.pixel_fraction
        total_area += area

        items_areas[item].append(area)

    return {item: sum(area) / total_area for item, area in items_areas.items()}


def my_image(path_or_image):
    if isinstance(path_or_image, str):
        my_image = build_image(path_or_image)
    elif isinstance(path_or_image, Image.Image):
        buffered = BytesIO()
        path_or_image.save(buffered, format="JPEG")
        my_image = types.Image(content=base64.b64encode(buffered.getvalue()))
    else:
        my_image = path_or_image

    return my_image


def localize_objects(path_or_image):
    """Localize objects in the local image.

    Args:
    path_or_image: The path to the local file or types.image
    """
    response = client.object_localization(image=my_image(path_or_image))
    objects = response.localized_object_annotations

    return {obj.name: obj.bounding_poly.normalized_vertices for obj in objects}


def localize_logos(path_or_image):
    """Localize logos in the local image.

    Args:
    path_or_image: The path to the local file or types.image
    """

    response = client.logo_detection(image=my_image(path_or_image))
    logos = response.logo_annotations

    return {logo.name: logo for logo in logos}


def detect_labels(path_or_image):
    """Localize labels in the local image.

    Args:
    path_or_image: The path to the local file or types.image
    """

    response = client.label_detection(image=my_image(path_or_image))
    labels = response.label_annotations

    return {label.description: label.score for label in labels}


def detect_prices(path_or_image, min_price=.1, max_price=10.):
    response = client.text_detection(image=my_image(path_or_image))
    objects = [obj for obj in response.text_annotations]

    prices = {}
    for object_ in objects:
        try:
            price = float(object_.description.replace(',', '.'))
        except ValueError:
            price = -9999.

        if min_price < price < max_price:
            prices[str(price)] = object_.bounding_poly.vertices

    return prices
