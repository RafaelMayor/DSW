import uuid

from django.conf import settings
from django.db import models


class Order(models.Model):
    class Status(models.IntegerChoices):
        INITIATED = 1
        CONFIRMED = 2
        PAID = 3
        CANCELLED = -1

    status = models.SmallIntegerField(choices=Status, default=Status.INITIATED)
    key = models.UUIDField(default=uuid.uuid4)
    games = models.ManyToManyField('games.Game', related_name='orders')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_orders'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def price(self):
        return sum(game.price for game in self.games.all())

    def __str__(self):
        return f'{self.key}'
