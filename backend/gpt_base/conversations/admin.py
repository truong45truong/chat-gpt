
from django.contrib import admin
from gpt_base.conversations.models import Conversations, Chat

# Register your models here.

class ConversationsAdmin(admin.ModelAdmin):
    model = Conversations
    list_display = ['id', 'name']
admin.site.register(Conversations, ConversationsAdmin)

class ChatAdmin(admin.ModelAdmin):
    model = Chat
    list_display = ['id', 'prompt', 'content', 'role']
    search_fields = ['conversation__pk']
admin.site.register(Chat, ChatAdmin)
