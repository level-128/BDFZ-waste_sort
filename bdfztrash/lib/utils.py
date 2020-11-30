import base64
import json
import socket
import urllib.parse
import urllib.request
from urllib.error import URLError, HTTPError
from .config.config_library import config

socket.setdefaulttimeout(config["timeout"])


def request_token(_url, _data, token):
    _headers = {
        "Content-Type": "application/json",
        "X-Auth-Token": token
    }

    data = bytes(json.dumps(_data), 'utf8')
    kreq = urllib.request.Request(_url, data, _headers)

    r = urllib.request.urlopen(kreq)
    status_code = r.code
    resp = r.read()
    return status_code, resp


def get_response(_url, auth_data):
    _headers = {
        'Content-Type': 'application/json'
    }

    data = json.dumps(auth_data).encode('utf8')
    req = urllib.request.Request(_url, data, _headers)
    return urllib.request.urlopen(req)


def get_token():
    auth_data = {
        "auth": {
            "identity": {

                "password": {
                    "user": {
                        "name": config["name"],
                        "password": config["password"],
                        "domain": {
                            "name": config["name"]
                        }
                    }
                },
                "methods": [
                    "password"
                ]
            },
            "scope": {
                "project": {
                    "name": config["region"]
                }
            }
        }
    }

    _url = config["tokens_url"]

    resp = get_response(_url, auth_data)
    X_TOKEN = resp.headers['X-Subject-Token']
    return X_TOKEN


def image_tagging(token, image, url, limit=-1, threshold=0.0):
    _url = config["image_tagging_url"]
    if image:
        image = image.decode("utf-8")

    _data = {
        "image": image,
        "url": url,
        "language": 'zh',
        "limit": limit,
        "threshold": threshold
    }

    status_code, resp = request_token(_url, _data, token)
    return resp.decode('unicode_escape')
