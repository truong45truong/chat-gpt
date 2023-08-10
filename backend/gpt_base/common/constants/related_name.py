from enum import Enum


class RelatedName(Enum):
    USERS = "users"
    USER_MEMBERS = "user_members"
    MEMBERS_USER = "members_user"
    MEMBERS_CONVERSATIONS = "members_conversions"
    MEMBERS_PROMPTS = "members_prompts"
    CONVERSATIONS_CHATS = "conversations_chats"
    WORKBOOKS_MEMBERS = 'workbooks_members'
    DOCUMENTS_WORKBOOK = 'documents_workbooks'
    DOCUMENTS_TEMPLATES  = 'documents_templates'
    DOCUMENTS_MEMBERS = "documents_members"