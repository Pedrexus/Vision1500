import os

from analysis.vision_algorithm._activate_api import build_image, client
from analysis.vision_algorithm.image_edition import crop_by_color, crop_to_hint
from analysis.vision_algorithm.image_properties import localize_logos, \
    detect_labels

TEMP = os.path.join(
    r'C:\Users\Pedro\Documents\PycharmProjects\Vision1500\static\images\temps',
    r'db37d329dh2938hd28h12812dwew.jpg')


def my_find_items(image_path, color='coca_cola_red', aspect_ratio=.55):
    crop_by_color(image_path, color=color, aspect_ratios=str(aspect_ratio),
                  output=TEMP, rethint=False)
    crop_to_hint(build_image(TEMP), TEMP,
                 aspect_ratios=str(1.8 * aspect_ratio), filename=TEMP)
    crop_to_hint(build_image(TEMP), TEMP,
                 aspect_ratios=str(2.7 * aspect_ratio), filename=TEMP)

    labels = detect_labels(TEMP)
    items = dict(labels)

    logos = localize_logos(TEMP)
    items.update(logos)

    return items


def detect_text(image_path, color, aspect_ratio):
    crop_by_color(image_path, color=color, aspect_ratios=str(aspect_ratio),
                  output=TEMP, rethint=False)

    words = client.document_text_detection(build_image(TEMP))

    return [word.description for word in words.text_annotations]


class Item:

    def __init__(self, image_path, color):
        self.aspect_ratio = .55 if 'red' in color else .25
        self.items = my_find_items(image_path, color, self.aspect_ratio)
        self.text = detect_text(image_path, color, self.aspect_ratio)

    @property
    def logo(self):
        coca_cola = ['coca', 'cola', 'coca cola']
        if any([item for item in self.items if item in coca_cola]):
            return 'coca-cola'
        elif [[letter for letter in set(word) if letter in {'F', 'N', 'T'}] for
              word in
              set(self.text)]:
            return 'fanta'


"""
def find_items(image_path, color, aspect_ratio=.75):
    img = crop_by_color(
        image_path,
        color=color,
        aspect_ratios=str(aspect_ratio),
        output=None,
        rethint=False,
        retimg=True
    )

    logos = localize_logos(img)
    labels = detect_labels(img)
    items = dict(labels)
    items.update(logos)

    img = crop_to_hint(
        img,
        img,
        aspect_ratios=str(1.8 * aspect_ratio),
        filename=None,
        retimg=True,
    )

    logos = localize_logos(img)
    items.update(logos)
    labels = detect_labels(img)
    items.update(labels)

    return items
"""
