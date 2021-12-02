import requests
import rest_framework.status as status
from core.models import User

from reviewch.settings import DEBUG

BASE_URL = 'http://localhost:8000/api/'
if not DEBUG:
    BASE_URL = 'https://glacial-reef-73763.herokuapp.com/api/'


def create_user(raw_data):
    url = f'{BASE_URL}users/'
    return requests.post(url, json=raw_data)


def create_review(raw_data):
    raw_data = raw_data.copy()
    raw_data['tags'] = raw_data['tags'].split()
    raw_data['author_id'] = User.objects.get(username=raw_data['user']).id
    url = f'{BASE_URL}reviews/'
    return requests.post(url, json=raw_data)


def update_review(raw_data, review_id):
    raw_data = raw_data.copy()
    raw_data['tags'] = raw_data['tags'].strip().split()
    raw_data['author_id'] = User.objects.get(username=raw_data['user']).id
    url = f'{BASE_URL}reviews/{review_id}/'
    return requests.put(url, json=raw_data)


def get_review(id: int):
    url = f'{BASE_URL}reviews/{id}/'
    return requests.get(url)


def create_comment(raw_data):
    url = f'{BASE_URL}comments/'
    return requests.post(url, json=raw_data)


def create_review_images(raw_data, files):
    res = requests.Response()
    data = dict()
    data['review_id'] = raw_data['id']
    for image in files.getlist('images'):
        data['image'] = image
        url = f'{BASE_URL}upload_images/'
        res = requests.post(url, files=data)
        if res.status_code != status.HTTP_201_CREATED:
            break
    return res
