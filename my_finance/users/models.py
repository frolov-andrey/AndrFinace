from django.contrib.auth import get_user_model
from django.db import models


class Profile(models.Model):

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    password = models.CharField(max_length=255)
    is_demo = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
