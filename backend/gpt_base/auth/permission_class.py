import logging

from django.conf import settings
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated, BasePermission


logger = logging.getLogger(__name__)


# Custom permission for users in token is exists.
class IsTokenValid(BasePermission):
    """
    Allows access only to user in token is exists.
    """
    message = {'message': 'Token is invalid or expired.'}
    
    def has_permission(self, request, view):
        return request.user
    
def is_authenticated(request):
    return request.user.is_authenticated


class IsUserAuthenticated(IsAuthenticated):

    def has_permission(self, request, view):
        return is_authenticated(request)