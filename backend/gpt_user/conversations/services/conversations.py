import logging

from gpt_base.common.constants.db_fields import DBConversationsFields, DBChatsFields
from gpt_base.conversations.models import Conversations, Chat
from gpt_base.members.models import Members
from gpt_base.conversations.services.conversations import ConversationsBaseService

__all__ = ['ConversationsService']

logger = logging.getLogger(__name__)


class ConversationsService:
    def __init__(self):
        super(ConversationsService, self).__init__()
        self.__conversations_service = ConversationsBaseService()

    #####################################################################################
    # Public methods
    #####################################################################################
    def get_list(self):
        # check conversation param has permission
        
        return
