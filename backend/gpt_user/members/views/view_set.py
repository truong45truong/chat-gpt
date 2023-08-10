# from django.db.models.functions import Concat
# from django_filters.rest_framework import DjangoFilterBackend
# from drf_spectacular.utils import OpenApiParameter, extend_schema
# from rest_framework import viewsets
# from rest_framework.decorators import action
# from rest_framework.filters import OrderingFilter
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response

# from gpt_base.auth.permissions.permission_class import IsClientAuthenticated
# from gpt_base.client.models import Client
# from gpt_base.client.serializers.client import ClientSettingMailDeliverySerializer, ClientAvatarSerializer, \
#     ClientUpdateAvatarSerializer
# from gpt_base.common.constants.db_fields import DBUserFields, DBClientGroupFields
# from gpt_base.common.constants.db_table import DBTable
# from gpt_base.common.constants.master import ClientStatusEnum
# from gpt_base.common.constants.view_action import ClientExtraViewSetAction, ViewSetAction
# from gpt_base.common.utils.exceptions import PermissionDenied
# from backend.gpt_user.user.serializers.user import ClientCreateUpdateSerializer, ClientsBasicSearchSerializer
# from gpt_user.user.services.client import ClientService


# class ClientViewSet(viewsets.ModelViewSet):
#     queryset = Client.objects.all()
#     serializer_classes = ClientCreateUpdateSerializer
#     permission_classes = (AllowAny,)
#     # ordering = f'-{DBUserFields.ID.value}'
#     # filter_backends = (DjangoFilterBackend, CustomSearchFilter, OrderingFilter)
#     # search_fields = 

#     def get_permissions(self):
#         handle_permissions_classes = {
#             ClientExtraViewSetAction.UPDATE_CLIENT: (IsClientAuthenticated,),
#             ClientExtraViewSetAction.CLIENTS_FINISH_REGISTER: (AllowAny,),
#             ClientExtraViewSetAction.SETTING_MAIL_DELIVERY: (IsClientAuthenticated,),
#             ViewSetAction.BASIC_CLIENTS_LIST: (AllowAny,),
#             ClientExtraViewSetAction.CLIENT_AVATAR: (IsClientAuthenticated,),
#             ClientExtraViewSetAction.UPDATE_CLIENT_AVATAR: (IsClientAuthenticated,),
#         }
#         permissions_classes = handle_permissions_classes.get(self.action)

#         if permissions_classes:
#             return [permission() for permission in permissions_classes]
#         else:
#             raise PermissionDenied()

#     def get_serializer_class(self):
#         serializer_classes = {
#             ClientExtraViewSetAction.UPDATE_CLIENT: ClientCreateUpdateSerializer,
#             ClientExtraViewSetAction.SETTING_MAIL_DELIVERY: ClientSettingMailDeliverySerializer,
#             ViewSetAction.BASIC_CLIENTS_LIST: ClientsBasicSearchSerializer,
#             ClientExtraViewSetAction.CLIENT_AVATAR: ClientAvatarSerializer,
#             ClientExtraViewSetAction.UPDATE_CLIENT_AVATAR: ClientUpdateAvatarSerializer,
#         }
#         return serializer_classes.get(self.action, ClientCreateUpdateSerializer)

#     def get_queryset(self):
#         queryset = Client.objects.annotate(
#             company_name=Concat(F'{DBTable.CLIENT_GROUP.value}__{DBClientGroupFields.COMPANY_NAME.value}', None),
#         )
#         return queryset

#     def update_client(self, request, *args, **kwargs):
#         instance = self.get_queryset().get(pk=request.user.id)
#         request.data[DBUserFields.CLIENT_GROUP.value][DBClientGroupFields.ID.value] = instance.client_group_id
#         client_service = ClientService()
#         res = client_service.update_client(instance, request.data)
#         return Response(res)

#     def setting_mail_delivery(self, request, *args, **kwargs):
#         instance = self.get_queryset().get(pk=request.user.id)
#         serializer = ClientSettingMailDeliverySerializer(instance, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)

#     @action(detail=False, methods=['GET'])
#     def clients_finish_register(self, *args, **kwargs):
#         clients = self.queryset.filter(status_id=ClientStatusEnum.BYPASS_CENSORSHIP.value).count()
#         return Response(dict(sumary=clients))

#     @extend_schema(parameters=[OpenApiParameter(name='search')])
#     def basic_clients_list(self, request, *args, **kwargs):
#         return super(ClientViewSet, self).list(self, request, *args, **kwargs)

#     @action(detail=False, methods=['GET'])
#     def get_client_avatar(self, request, *args, **kwargs):
#         instance = self.get_queryset().get(pk=request.user.id)
#         serializer = ClientAvatarSerializer(instance.client_group)
#         return Response(serializer.data)

#     @action(detail=False, methods=['PUT'])
#     def update_client_avatar(self, request, *args, **kwargs):
#         instance = self.get_queryset().get(pk=request.user.id)
#         serializer = ClientUpdateAvatarSerializer(instance.client_group, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
