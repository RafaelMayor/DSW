from django.db import models


class Platform(models.Model):
    name = models.TextField(unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(blank=True, upload_to='logos', default='logos/default.jpg')

    def __str__(self):
        return f'{self.name}'
