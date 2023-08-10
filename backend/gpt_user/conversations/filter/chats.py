import django_filters

from gpt_base.common.constants.db_fields import DBChatsFields
from gpt_base.conversations.models import Chat


class ChatListFilterSet(django_filters.FilterSet):
    conversation_id = django_filters.NumberFilter(field_name=DBChatsFields.CONVERSATION_ID.value)

    class Meta:
        model = Chat
        fields = (
            DBChatsFields.CONVERSATION_ID.value,
        )
