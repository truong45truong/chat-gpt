from django.urls import path

from gpt_user.chat_gpt.views import view_api
# from gpt_user.user.views.view_set import ClientViewSet

urlpatterns = [
    path('process', view_api.process, name='process-chat-gpt'),
]
