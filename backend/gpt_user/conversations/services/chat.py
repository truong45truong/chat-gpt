import logging

from gpt_base.common.constants.db_fields import DBConversationsFields, DBChatsFields
from gpt_base.conversations.models import Conversations, Chat
from gpt_base.members.models import Members
from gpt_base.conversations.services.chat import ChatBaseService
from gpt_base.common.utils.exceptions import CustomAPIException

__all__ = ['ChatService']

logger = logging.getLogger(__name__)


class ChatService:
    def __init__(self):
        super(ChatService, self).__init__()
        self.__chat_service = ChatBaseService()

    #####################################################################################
    # Public methods
    #####################################################################################
    def get_list(self, user, filtered_qs, serializer, conversation_id):
        # check conversation param has permission
        conversations = Conversations.objects.filter(pk=conversation_id, member__user=user)
        if not conversations.exists():
            raise CustomAPIException(detail="Conversation does not exist or user has no permission access", 
                                     message_code="CONVERSATION_NOT_FOUND", status_code=404)
        
        # get list
        serializer_data = serializer(filtered_qs, many=True)
        
        return {"data": serializer_data.data}
