from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from gpt_base.common.constants.db_fields import DBMembersFields
from gpt_base.user.serializers.user import UserInfoSerializer
from gpt_base.members.models import Members

class MembersDetailUpdateSerializer(WritableNestedModelSerializer):
    user = UserInfoSerializer(many=False)

    class Meta:
        model = Members
        fields = (
            DBMembersFields.ID.value, 
            DBMembersFields.USER.value, 
            DBMembersFields.TOKEN_LIMIT.value, 
            DBMembersFields.QUANTITY_TOKEN_USED.value, 
        )