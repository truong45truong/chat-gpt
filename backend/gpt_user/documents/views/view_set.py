from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from gpt_base.auth.permission_class import IsUserAuthenticated
from gpt_base.documents.models.documents import Templates ,WorkBooks,Documents

from gpt_base.common.constants.view_action import ViewSetAction
from gpt_base.common.utils.exceptions import PermissionDenied
from gpt_user.documents.serializers.documents import (
    TemplateDetailListSerializer,
    TemplateDetailSerializer,
    WorkBookDetailListSerializer,
    DocumentsCreateSerializer,
    DocumentsDetailListSerializer,
    DocumentsUpdateSerializer,
    DocumentsDetailSerializer,
    WorkBooksCreateSerializer,
    WorkBooksUpdateSerializer
)

class TemplatesViewSet(
    mixins.CreateModelMixin, 
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin, 
    mixins.RetrieveModelMixin, 
    viewsets.GenericViewSet
):
    queryset = Templates.objects.all()
    serializer_classes = TemplateDetailListSerializer
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
            ViewSetAction.LIST.value: TemplateDetailListSerializer,
            ViewSetAction.DETAIL.value: TemplateDetailSerializer,
        }
        return serializer_classes.get(self.action, TemplateDetailListSerializer)

    def get_queryset(self):
        return Templates.objects.filter().order_by("-pk")

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data})


class WorkBooksViewSet(
    mixins.CreateModelMixin, 
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin, 
    mixins.RetrieveModelMixin, 
    viewsets.GenericViewSet
):
    queryset = WorkBooks.objects.all()
    serializer_classes = WorkBookDetailListSerializer
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
            ViewSetAction.LIST.value: WorkBookDetailListSerializer,
            ViewSetAction.CREATE.value: WorkBooksCreateSerializer,
            ViewSetAction.DETAIL.value: WorkBookDetailListSerializer,
            ViewSetAction.UPDATE.value: WorkBooksUpdateSerializer,
        }
        return serializer_classes.get(self.action, WorkBookDetailListSerializer)

    def get_queryset(self):
        return WorkBooks.objects.filter(member__user=self.request.user).order_by("-pk")
    def create(self, request):
        data = self.get_serializer().create(
            validated_data=request.data, user = request.user
        )
        return Response(data=data)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data})
class DocumentsViewSet(
    mixins.CreateModelMixin, 
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin, 
    mixins.RetrieveModelMixin, 
    viewsets.GenericViewSet
):
    queryset = Documents.objects.all()
    serializer_classes = DocumentsDetailListSerializer
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
            ViewSetAction.CREATE.value: DocumentsCreateSerializer,
            ViewSetAction.LIST.value: DocumentsDetailListSerializer,
            ViewSetAction.DETAIL.value: DocumentsDetailSerializer,
            ViewSetAction.UPDATE.value: DocumentsUpdateSerializer,
        }
        return serializer_classes.get(self.action, DocumentsDetailListSerializer)

    def get_queryset(self):
        return Documents.objects.filter(member__user=self.request.user).order_by("-pk")
    
    def create(self, request):
        data = self.get_serializer().create(
            validated_data=request.data, user = request.user,
            workbook_id = request.data['workbook_id'],
            template_id = request.data['template_id'],
        )
        return Response(data=data)

    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"data": serializer.data})