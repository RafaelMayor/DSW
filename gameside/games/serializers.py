from categories.serializers import CategoriesSerializer
from platforms.serializers import PlatformSerializer
from shared.serializers import BaseSerializer
from users.serializers import UsersSerializer


class GamesSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'title': instance.title,
            'slug': instance.slug,
            'description': instance.description,
            'cover': self.build_url(instance.cover.url),
            'price': float(instance.price),
            'stock': instance.stock,
            'released_at': instance.released_at.isoformat(),
            'pegi': instance.get_pegi_display(),
            'category': CategoriesSerializer(instance.category).serialize(),
            'platforms': PlatformSerializer(
                instance.platforms.all(), request=self.request
            ).serialize(),
        }


class ReviewsSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'rating': instance.rating,
            'comment': instance.comment,
            'game': GamesSerializer(instance.game, request=self.request).serialize(),
            'author': UsersSerializer(instance.author).serialize(),
            'created_at': instance.created_at.isoformat(),
            'updated_at': instance.updated_at.isoformat(),
        }
