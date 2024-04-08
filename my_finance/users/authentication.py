import random

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

from .models import Profile


class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()

        try:
            user = user_model.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None


class DemoAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()

        try:
            if username == 'demo' and password == 'demo':
                username = f'demo{random.randint(1, 1000)}'
                password = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',
                                                  k=10))  # Random password
                user, created = get_user_model().objects.get_or_create(username=username)
                if created:
                    user.set_password(password)
                    user.save()
                    Profile.objects.create(user=user, password=password, is_demo=True)
                else:
                    return None
            else:
                return None

            if user.check_password(password):
                return user
            return None
        except (user_model.DoesNotExist, user_model.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None
