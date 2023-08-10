from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class ForeignKeyField(serializers.IntegerField):

    def __init__(self, model, **kwargs):
        self.model = model
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        if not data:
            return None

        try:
            obj = self.model.objects.get(pk=data)
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Id does_not_exist')
        except (TypeError, ValueError):
            raise serializers.ValidationError('Id incorrect_type')

        return obj.id


class PaginationSerializers(serializers.Serializer):
    page = serializers.IntegerField(default=1)
    page_size = serializers.IntegerField(default=10)

