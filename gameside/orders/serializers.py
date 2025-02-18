from games.serializers import GamesSerializer
from shared.serializers import BaseSerializer
from users.serializers import UsersSerializer


class OrdersSerializer(BaseSerializer):
    def __init__(self, to_serialize, *, fields=[], request=None):
        super().__init__(to_serialize, fields=fields, request=request)

    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'status': instance.get_status_display(),
            'key': instance.key if instance.get_status_display() == 'PAID' else None,
            'games': GamesSerializer(instance.games.all(), request=self.request).serialize(),
            'user': UsersSerializer(instance.user).serialize(),
            'created_at': instance.created_at.isoformat(),
            'updated_at': instance.updated_at.isoformat(),
            'price': instance.price,
        }
