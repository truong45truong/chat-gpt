from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from gpt_base.conversations.models import Conversations, Chat
from gpt_base.common.constants.db_fields import DBConversationsFields, DBChatsFields
from gpt_base.common.utils.serializers import ForeignKeyField
from gpt_base.master.models import TranslateTypesMaster
from gpt_base.members.serializers.members import MembersDetailUpdateSerializer
from gpt_base.members.models import Members
from gpt_base.common.constants.master_data import TranslateTypesEnum
from gpt_base.common.constants.constant import RoleEnum

# Conversations
class ConversationsDetailListSerializer(serializers.ModelSerializer):
    # member = MembersDetailUpdateSerializer(many=False)

    class Meta:
        model = Conversations
        fields = (
            DBConversationsFields.ID.value,
            # DBConversationsFields.MEMBER.value,
            DBConversationsFields.NAME.value,
        )

class ConversationsCreateSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Conversations
        fields = (
            DBConversationsFields.NAME.value,
        )
        
    def create(self, validated_data, user):
        member = Members.objects.get(user=user)
        conversation = Conversations.objects.create(**validated_data, member=member)
        data = {
            "data": {
                "id": conversation.pk, 
                "name": conversation.name
            }
        }
        return data
        
class ConversationsUpdateSerializer(WritableNestedModelSerializer):
    class Meta:
        model = Conversations
        fields = (
            DBConversationsFields.NAME.value,
        )

# Chats
class ChatsDetailListSerializer(serializers.ModelSerializer):
    # conversation_id = ForeignKeyField(model=Conversations)
    # translate_type_id = ForeignKeyField(model=TranslateTypesMaster)
    is_inverse = serializers.SerializerMethodField('get_is_inverse')

    
    class Meta:
        model = Chat
        fields =(
            DBChatsFields.ID.value,
            # DBChatsFields.CONVERSATION_ID.value,
            DBChatsFields.PROMPT.value,
            DBChatsFields.CONTENT.value,
            # DBChatsFields.CONTENT_TRANSLATE.value,
            # DBChatsFields.TRANSLATE_TYPE_ID.value,
            DBChatsFields.ROLE.value,
            DBChatsFields.IS_INVERSE.value,
            DBChatsFields.CREATED_AT.value,
            DBChatsFields.UPDATED_AT.value,
        )
        
    def get_is_inverse(self, instance):
        if instance.role == RoleEnum.USER.value:
            return True
        elif instance.role == RoleEnum.ASSISTANT.value:
            return False
        return False

class ChatsCreateSerializer(WritableNestedModelSerializer):
    conversation_id = ForeignKeyField(model=Conversations)
    # translate_type_id = ForeignKeyField(model=TranslateTypesMaster, default=TranslateTypesEnum.ENGLISH.value)
    
    class Meta:
        model = Chat
        fields =(
            DBChatsFields.CONVERSATION_ID.value,
            DBChatsFields.PROMPT.value,
            DBChatsFields.CONTENT.value,
            # DBChatsFields.TRANSLATE_TYPE_ID.value,
            DBChatsFields.ROLE.value,
            DBChatsFields.CREATED_AT.value,
            DBChatsFields.UPDATED_AT.value,
        )


class ChatsUpdateSerializer(WritableNestedModelSerializer):
    conversation_id = ForeignKeyField(model=Conversations)
    translate_type_id = ForeignKeyField(model=TranslateTypesMaster)
    
    class Meta:
        model = Chat
        fields =(
            DBChatsFields.CONVERSATION_ID.value,
            DBChatsFields.PROMPT.value,
            DBChatsFields.CONTENT.value,
            DBChatsFields.CONTENT_TRANSLATE.value,
            DBChatsFields.TRANSLATE_TYPE_ID.value,
            DBChatsFields.ROLE.value,
            DBChatsFields.CREATED_AT.value,
            DBChatsFields.UPDATED_AT.value,
        )
