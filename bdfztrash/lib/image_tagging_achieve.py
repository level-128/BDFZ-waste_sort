import base64

from .utils import get_token, image_tagging
from .config.config_library import config
from urllib.error import URLError, HTTPError


def recognize_image(image_dir: str):
    try:
        token = get_token()
        image_b64 = encode_to_base64(image_dir)
        return image_tagging(token, image_b64, '', config['max_recognize_count'])
    except HTTPError as e:
        status_code = e.code
        raise SystemExit(f"HTTPError: {e.reason=}, {e.read()=}, {status_code=}")
    except URLError as e:
        raise SystemExit(f"URLError: {e.reason=}")


def encode_to_base64(filename: str):
    with open(filename, 'rb') as file:
        return base64.b64encode(file.read())

