from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from gpt_base.common.constants.db_fields import DBUserFields
from gpt_base.user.models import User


class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            DBUserFields.ID.value, 
            DBUserFields.EMAIL.value, 
            DBUserFields.FIRST_NAME.value,
            DBUserFields.LAST_NAME.value,
        )

class UserBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            DBUserFields.ID.value,
            DBUserFields.FIRST_NAME.value,
            DBUserFields.LAST_NAME.value,
        )
