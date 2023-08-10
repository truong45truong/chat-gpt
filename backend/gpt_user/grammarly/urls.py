from django.urls import path

from gpt_user.grammarly.views import view_api
# from gpt_user.user.views.view_set import ClientViewSet

urlpatterns = [
    path('check', view_api.check_grammarly, name='grammarly'),
]
