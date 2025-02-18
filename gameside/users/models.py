import uuid

from django.conf import settings
from django.db import models


class Token(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    key = models.UUIDField(default=uuid.uuid4)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='token'
    )

    def __str__(self):
        return f'{self.key}'
