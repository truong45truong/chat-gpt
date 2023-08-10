
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework_simplejwt.exceptions import AuthenticationFailed


class PermissionDenied(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'permission denied'
    default_code = '403'


class CustomerInvalidToken(AuthenticationFailed):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Token is invalid or expired'
    default_code = 'token_not_valid'

class CustomAPIException(APIException):
    def __init__(
        self,
        detail=_("Common error"),
        status_code=status.HTTP_400_BAD_REQUEST,
        message_code=None,
    ):
        self.detail = {"detail": detail, "message_code": message_code}
        self.status_code = status_code