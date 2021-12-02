import core.api_requests as api
from uuid import uuid4
import rest_framework.status as status
from social_core.pipeline.social_auth import social_details
from social_core.pipeline.user import create_user
from core.models import User

USER_FIELDS = ['username', 'email']


def create_user(strategy, details, backend, user=None, *args, **kwargs):
    if user:
        return {'is_new': False}

    fields = dict((name, kwargs.get(name, details.get(name)))
                  for name in backend.setting('USER_FIELDS', USER_FIELDS))

    if not fields:
        return

    if backend.name == 'facebook':

        if len(User.objects.filter(username=fields['username'].replace(' ', ''))) != 0:
            return {'is_new': False}

        data = {
            'username': fields['username'].replace(' ', ''),
            'email': fields['email'],
            'password': str(uuid4())
        }
        res = api.create_user(data)
        user_data = res.json()
        if res.status_code != status.HTTP_201_CREATED:
            raise Exception('Authentication failed')
        return {
            'is_new': True,
            'user': User.objects.get(pk=user_data['id'])
        }
    if backend.name == 'github':

        if len(User.objects.filter(username=fields['username'])) != 0:
            return {'is_new': False}

        data = {
            'username': fields['username'],
            'email': fields['email'],
            'password': str(uuid4())
        }
        res = api.create_user(data)
        user_data = res.json()
        if res.status_code != status.HTTP_201_CREATED:
            raise Exception('Authentication failed')
        return {
            'is_new': True,
            'user': User.objects.get(pk=user_data['id'])
        }
