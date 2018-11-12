import io
import os

from google.cloud import vision
from google.cloud.vision import types

GOOGLE_CLOUD_CREDENTIALS_JSON = r'C:\Users\Pedro\Documents\PycharmProjects\Vision1500\google_cloud_credentials.json'
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_CLOUD_CREDENTIALS_JSON


def build_image(image_path):
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    return image


client = vision.ImageAnnotatorClient()
