from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from gpt_user.members.serializers.registration import RegisterMembersSerializer
from gpt_user.members.services.registration import MemberRegistrationService


@extend_schema(
    methods=['POST'],
    tags=['members'],
    request=RegisterMembersSerializer,
    description='register caller',
    responses={200: None}
)
@api_view(["POST"])
@permission_classes([AllowAny])
def register(request):
    member_service = MemberRegistrationService()
    member_service.register_member(request.data)
    return Response(status=status.HTTP_200_OK)


