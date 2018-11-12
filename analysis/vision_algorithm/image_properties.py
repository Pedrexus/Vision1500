from collections import defaultdict

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


def localize_objects(path):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    response = client.object_localization(image=build_image(path))
    objects = response.localized_object_annotations

    return {obj.name: obj.bounding_poly.normalized_vertices for obj in objects}


def detect_prices(path, min_price=.1, max_price=10.):
    response = client.text_detection(image=build_image(path))
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