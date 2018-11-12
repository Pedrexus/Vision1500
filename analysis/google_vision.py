import os

# Imports the Google Cloud client library

GOOGLE_CLOUD_CREDENTIALS_JSON = r'C:\Users\Pedro\Documents\PycharmProjects\Vision1500\google_cloud_credentials.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_CLOUD_CREDENTIALS_JSON


def localize_objects(path):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        print('\n{} (confidence: {})'.format(object_.name, object_.score))
        print('Normalized bounding polygon vertices: ')
        for vertex in object_.bounding_poly.normalized_vertices:
            print(' - ({}, {})'.format(vertex.x, vertex.y))

# prices: client.text_detection
# itens:  client.logo_detection (maybe not working)
# labels: client.web_detection, client.label_detection
# colors: client.image_properties
