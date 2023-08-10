from django.urls import path

# from gpt_user.conversations.views import view_api
from gpt_user.documents.views.view_set import TemplatesViewSet , WorkBooksViewSet , DocumentsViewSet
from gpt_base.common.constants.view_action import ViewSetAction
from gpt_user.documents.views.view_api import process_generate_document , get_document_workbook
urlpatterns = [
    path('templates/list', view=TemplatesViewSet.as_view({'get': ViewSetAction.LIST.value})),
    path('templates/<int:pk>', view=TemplatesViewSet.as_view({'get': ViewSetAction.DETAIL.value})),
    path('templates/process-generate', process_generate_document),
    path('workbook/list', view=WorkBooksViewSet.as_view({'get': ViewSetAction.LIST.value})),
    path('workbook/<int:pk>/detail', view=WorkBooksViewSet.as_view({'get': ViewSetAction.DETAIL.value})),
    path('workbook/<int:pk>/update', view=WorkBooksViewSet.as_view({'put': ViewSetAction.UPDATE.value})),
    path('workbook/<int:pk>/delete', view=WorkBooksViewSet.as_view({'delete': ViewSetAction.DELETE.value})),
    path('workbook/create', view=WorkBooksViewSet.as_view({'post': ViewSetAction.CREATE.value})),
    path('list', view=DocumentsViewSet.as_view({'get': ViewSetAction.LIST.value})),
    path('create', view=DocumentsViewSet.as_view({'post': ViewSetAction.CREATE.value})),
    path('workbook/get-document', get_document_workbook),
    path('<int:pk>/detail', view=DocumentsViewSet.as_view({'get': ViewSetAction.DETAIL.value})),
    path('<int:pk>/update', view=DocumentsViewSet.as_view({'put': ViewSetAction.UPDATE.value})),
    path('<int:pk>/delete', view=DocumentsViewSet.as_view({'delete': ViewSetAction.DELETE.value})),
]
