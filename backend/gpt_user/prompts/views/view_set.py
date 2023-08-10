from django.db.models.functions import Concat
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from gpt_base.auth.permission_class import IsUserAuthenticated
from gpt_base.prompts.models.prompts import Prompts
from gpt_base.members.models.members import Members
from gpt_base.common.constants.db_fields import DBConversationsFields, DBChatsFields
from gpt_base.common.constants.db_table import DBTable
from gpt_base.common.constants.constant import RoleEnum
from gpt_base.common.constants.view_action import ViewSetAction, ConversationViewSetAction
from gpt_base.common.utils.exceptions import PermissionDenied
from gpt_user.prompts.serializers.prompts import (
    PromptsDetailListSerializer,
    PromptsCreateSerializer,
    PromptsUpdateSerializer
)
from gpt_user.conversations.services.conversations import ConversationsService
from gpt_user.conversations.services.chat import ChatService
from gpt_user.conversations.filter.chats import ChatListFilterSet


class PromptViewSet(
    mixins.CreateModelMixin, 
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin, 
    mixins.RetrieveModelMixin, 
    viewsets.GenericViewSet
):
    queryset = Prompts.objects.all()
    serializer_classes = PromptsDetailListSerializer
    permission_classes = (IsUserAuthenticated,)

    def get_permissions(self):
        handle_permissions_classes = {
            ViewSetAction.CREATE.value: (IsUserAuthenticated,),
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
            ViewSetAction.CREATE.value: PromptsCreateSerializer,
            ViewSetAction.LIST.value: PromptsDetailListSerializer,
            ViewSetAction.DETAIL.value: PromptsDetailListSerializer,
            ViewSetAction.UPDATE.value: PromptsUpdateSerializer,
        }
        return serializer_classes.get(self.action, PromptsDetailListSerializer)

    def get_queryset(self):
        return Prompts.objects.filter(member__user=self.request.user).order_by("-pk")
    
    def create(self, request):
        data = self.get_serializer().create(validated_data=request.data, user = request.user)
        return Response(data=data)

    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data})

