from enum import Enum


class VerboseNamePlural(str, Enum):
    USER = 'users'
    MEMBERS = 'members'
    CONVERSATIONS = 'conversations'
    CHATS = 'chats'
    PROMPTS ='prompts'
    WORK_BOOKS = 'work_books'
    DOCUMENTS = 'documents'
    TEMPLATES = 'templates'