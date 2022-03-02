from uuid import uuid4

from core.models import User
from core.services import UserService

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

        user = UserService.create(data)
        return {
            'is_new': True,
            'user': User.objects.get(pk=user.id)
        }
    if backend.name == 'github':

        if len(User.objects.filter(username=fields['username'])) != 0:
            return {'is_new': False}

        data = {
            'username': fields['username'],
            'email': fields['email'],
            'password': str(uuid4())
        }

        user = UserService.create(data)
        return {
            'is_new': True,
            'user': User.objects.get(pk=user.id)
        }
