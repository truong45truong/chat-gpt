from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from gpt_base.common.constants.db_fields import DBConversationsFields
from gpt_base.members.serializers.members import MembersDetailUpdateSerializer
from gpt_base.conversations.models import Conversations

class ConversationsDetailUpdateSerializer(WritableNestedModelSerializer):
    member = MembersDetailUpdateSerializer(many=False)

    class Meta:
        model = Conversations
        fields = (
            DBConversationsFields.ID.value, 
            DBConversationsFields.MEMBER.value, 
            DBConversationsFields.NAME.value, 
        )

