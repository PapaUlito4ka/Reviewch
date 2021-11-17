import requests
import json
from reviewch.settings import DEBUG

BASE_URL = 'http://localhost:8000/api/'
if not DEBUG:
    BASE_URL = 'https://glacial-reef-73763.herokuapp.com/api/'


def create_user(raw_data):
    url = f'{BASE_URL}users/'
    return requests.post(url, data=raw_data)

