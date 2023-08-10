from django.urls import path

# from gpt_user.conversations.views import view_api
from gpt_user.conversations.views.view_set import ConversationViewSet, ChatViewSet
from gpt_base.common.constants.view_action import ViewSetAction, ConversationViewSetAction

urlpatterns = [
    # Conversations
    path('list', view=ConversationViewSet.as_view({'get': ViewSetAction.LIST.value})),
    path('<int:pk>/detail', view=ConversationViewSet.as_view({'get': ViewSetAction.DETAIL.value})),
    path('<int:pk>/update', view=ConversationViewSet.as_view({'put': ViewSetAction.UPDATE.value})),
    path('<int:pk>/delete', view=ConversationViewSet.as_view({'delete': ViewSetAction.DELETE.value})),
    path('<int:id>/delete-all-chat', view=ConversationViewSet.as_view({'delete': ConversationViewSetAction.DELETE_ALL_CHAT.value})),
    path('create', view=ConversationViewSet.as_view({'post': ViewSetAction.CREATE.value})),
    # Chats
    path('chat/list', view=ChatViewSet.as_view({'get': ViewSetAction.LIST.value})),
    path('chat/<int:pk>/detail', view=ChatViewSet.as_view({'get': ViewSetAction.DETAIL.value})),
    path('chat/<int:pk>/update', view=ChatViewSet.as_view({'put': ViewSetAction.UPDATE.value})),
    path('chat/<int:pk>/delete', view=ChatViewSet.as_view({'delete': ViewSetAction.DELETE.value})),
    
]
