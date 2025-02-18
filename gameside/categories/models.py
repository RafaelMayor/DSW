from colorfield.fields import ColorField
from django.db import models


class Category(models.Model):
    name = models.TextField(unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    color = ColorField(default='#ffffff', blank=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return f'{self.name}'
