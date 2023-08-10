from enum import Enum


class ViewSetAction(str, Enum):
    LIST = 'list'
    LIST_BASIC = 'list_basic'
    DETAIL = 'retrieve'
    CREATE = 'create'
    UPDATE = 'update'
    DELETE = 'destroy'

class ConversationViewSetAction(str, Enum):
    DELETE_ALL_CHAT = 'delete_all_chat'