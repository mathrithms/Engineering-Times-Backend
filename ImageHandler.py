from django.conf import settings
import os
import requests
from pathlib import Path
from PIL import Image

BASE_DIR = Path(__file__).resolve().parent


def crop(image, required_width, required_height):
    original_width, original_height = image.size

    original_ratio = original_width / original_height
    required_ratio = required_width / required_height

    if abs(original_ratio - required_ratio) < 0.1:
        return image

    elif original_ratio > required_ratio:
        new_height = original_height
        new_width = int((required_width * original_height) / required_height)

    else:
        new_width = original_width
        new_height = int((required_height * original_width) / required_width)

    left = (original_width - new_width) / 2
    top = (original_height - new_height) / 2
    right = (original_width + new_width) / 2
    bottom = (original_height + new_height) / 2

    return image.crop((left, top, right, bottom))


def resize_upload(file_name, cdn_folder, cdn_name, new_size=None):
    path = os.path.join(BASE_DIR, 'media')
    path = os.path.join(path, file_name)

    if os.path.exists(path) and len(file_name) != 0:

        if new_size is not None:
            im = Image.open(path)
            im = crop(im, new_size[0], new_size[1])
            resized_im = im.resize((new_size[0], new_size[1]),
                                   resample=Image.LANCZOS)
            resized_im.save(path)

        with open(path, 'rb') as file:
            file_data = file.read()

        extension = file_name.split('.')[-1]

        request_url = settings.CDN_BASE_URL + cdn_folder \
            + '/' + cdn_name + '.' + extension

        header = {
            'AccessKey': settings.BUNNY_STORAGE_KEY
        }

        response = requests.request('PUT', request_url,
                                    data=file_data, headers=header)

        if response.status_code != 201:
            raise Exception('Some error with CDN')

        os.remove(path)

        return cdn_folder + '/' + cdn_name + '.' + extension
