from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Game(models.Model):
    class Pegi(models.IntegerChoices):
        PEGI3 = 3
        PEGI7 = 7
        PEGI12 = 12
        PEGI16 = 16
        PEGI18 = 18

    title = models.TextField(unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    cover = models.ImageField(blank=True, upload_to='covers', default='covers/default.jpg')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    stock = models.PositiveIntegerField()
    released_at = models.DateField()
    pegi = models.PositiveSmallIntegerField(choices=Pegi)
    category = models.ForeignKey(
        'categories.Category', on_delete=models.SET_NULL, null=True, related_name='games'
    )
    platforms = models.ManyToManyField('platforms.Platform', related_name='platform_games')

    def __str__(self):
        return f'{self.title}'


class Review(models.Model):
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    game = models.ForeignKey('games.Game', on_delete=models.CASCADE, related_name='game_reviews')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_reviews'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.rating} - {self.comment}'
