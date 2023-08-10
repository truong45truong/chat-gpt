from django.urls import path

# from gpt_user.conversations.views import view_api
from gpt_user.prompts.views.view_set import PromptViewSet
from gpt_base.common.constants.view_action import ViewSetAction

urlpatterns = [
    path('list', view=PromptViewSet.as_view({'get': ViewSetAction.LIST.value})),
    path('create', view=PromptViewSet.as_view({'post': ViewSetAction.CREATE.value})),
    path('<int:pk>/detail', view=PromptViewSet.as_view({'get': ViewSetAction.DETAIL.value})),
    path('<int:pk>/update', view=PromptViewSet.as_view({'put': ViewSetAction.UPDATE.value})),
    path('<int:pk>/delete', view=PromptViewSet.as_view({'delete': ViewSetAction.DELETE.value})),
]
