from django.db.models.functions import Concat
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from gpt_base.auth.permission_class import IsUserAuthenticated
from gpt_base.conversations.models import Conversations, Chat
from gpt_base.common.constants.db_fields import DBConversationsFields, DBChatsFields
from gpt_base.common.constants.db_table import DBTable
from gpt_base.common.constants.constant import RoleEnum
from gpt_base.common.constants.view_action import ViewSetAction, ConversationViewSetAction
from gpt_base.common.utils.exceptions import PermissionDenied
from gpt_user.conversations.serializers.conversations import (
    ConversationsDetailListSerializer,
    ConversationsCreateSerializer,
    ConversationsUpdateSerializer,
    ChatsUpdateSerializer,
    ChatsDetailListSerializer,
)
from gpt_user.conversations.services.conversations import ConversationsService
from gpt_user.conversations.services.chat import ChatService
from gpt_user.conversations.filter.chats import ChatListFilterSet


class ConversationViewSet(
    mixins.CreateModelMixin, 
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin, 
    mixins.RetrieveModelMixin, 
    viewsets.GenericViewSet
):
    queryset = Conversations.objects.all()
    serializer_classes = ConversationsDetailListSerializer
    permission_classes = (IsUserAuthenticated,)

    def get_permissions(self):
        handle_permissions_classes = {
            ViewSetAction.CREATE.value: (IsUserAuthenticated,),
            ViewSetAction.LIST.value: (IsUserAuthenticated,),
            ViewSetAction.DELETE.value: (IsUserAuthenticated,),
            ViewSetAction.DETAIL.value: (IsUserAuthenticated,),
            ViewSetAction.UPDATE.value: (IsUserAuthenticated,),
            ConversationViewSetAction.DELETE_ALL_CHAT.value: (IsUserAuthenticated,),
        }
        permissions_classes = handle_permissions_classes.get(self.action)

        if permissions_classes:
            return [permission() for permission in permissions_classes]
        else:
            raise PermissionDenied()

    def get_serializer_class(self):
        serializer_classes = {
            ViewSetAction.CREATE.value: ConversationsCreateSerializer,
            ViewSetAction.LIST.value: ConversationsDetailListSerializer,
            ViewSetAction.DETAIL.value: ConversationsDetailListSerializer,
            ViewSetAction.UPDATE.value: ConversationsUpdateSerializer,
        }
        return serializer_classes.get(self.action, ConversationsDetailListSerializer)

    def get_queryset(self):
        return Conversations.objects.filter(member__user=self.request.user).order_by("-pk")
    
    def create(self, request):
        data = self.get_serializer().create(validated_data=request.data, user=request.user)
        return Response(data=data)

    def delete_all_chat(self, request, id, **kwargs):
        Chat.objects.filter(conversation_id=id, conversation__member__user=self.request.user)
        return Response(data={})
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data}) 

class ChatViewSet(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin, 
    mixins.RetrieveModelMixin, 
    viewsets.GenericViewSet
):
    queryset = Chat.objects.all()
    serializer_classes = ChatsDetailListSerializer
    permission_classes = (IsUserAuthenticated,)
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filterset_class = ChatListFilterSet
    

    def get_permissions(self):
        handle_permissions_classes = {
            ViewSetAction.LIST.value: (IsUserAuthenticated,),
            ViewSetAction.DELETE.value: (IsUserAuthenticated,),
            ViewSetAction.DETAIL.value: (IsUserAuthenticated,),
            ViewSetAction.UPDATE.value: (IsUserAuthenticated,),
        }
        permissions_classes = handle_permissions_classes.get(self.action)

        if permissions_classes:
            return [permission() for permission in permissions_classes]
        else:
            raise PermissionDenied()

    def get_serializer_class(self):
        serializer_classes = {
            ViewSetAction.LIST.value: ChatsDetailListSerializer,
            ViewSetAction.DETAIL.value: ChatsDetailListSerializer,
            ViewSetAction.UPDATE.value: ChatsUpdateSerializer,
        }
        return serializer_classes.get(self.action, ChatsDetailListSerializer)

    def get_queryset(self):
        return Chat.objects.filter(
            role__in=(RoleEnum.USER.value, RoleEnum.ASSISTANT.value), 
            conversation__member__user=self.request.user
            ).order_by('pk')
    
    def list(self, request):
        chat_service = ChatService()
        filtered_qs = self.filterset_class(request.GET, queryset=self.get_queryset()).qs
        data = chat_service.get_list(self.request.user, filtered_qs, self.get_serializer, request.GET.get('conversation_id'))
        return Response(data=data)