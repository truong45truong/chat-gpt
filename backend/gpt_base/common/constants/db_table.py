from enum import Enum


class DBTable(str, Enum):
    USER = 'user'
    MEMBERS = 'members'
    CONVERSATIONS = 'conversations'
    CHATS = 'chats'
    PROMPTS = 'prompts'
    # data master
    M_TRANSLATE_TYPES = 'm_translate_types'
    WORK_BOOKS = 'work_books'
    DOCUMENTS = 'documents'
    TEMPLATES = 'templates'