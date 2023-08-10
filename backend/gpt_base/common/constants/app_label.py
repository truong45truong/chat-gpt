from enum import Enum


class ModelAppLabel(str, Enum):
    USER = 'user'
    MEMBERS = 'members'
    CONVERSATIONS = 'conversations'
    CHATS = 'chats'
    MASTER = 'master'
    PROMPTS = 'prompts'
    WORK_BOOKS = 'work_books'
    DOCUMENTS = 'documents'
    TEMPLATES = 'templates'