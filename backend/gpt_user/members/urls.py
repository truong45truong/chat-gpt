from django.urls import path

from gpt_user.members.views import view_api
# from gpt_user.user.views.view_set import ClientViewSet

urlpatterns = [
    path('register', view_api.register, name='register-member'),
]
