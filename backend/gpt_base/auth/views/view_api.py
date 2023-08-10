from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from gpt_base.auth.permission_class import IsUserAuthenticated
from gpt_base.auth.serializers import ResetPasswordSerializer, ForgotPasswordSerializer, ChangePasswordSerializer, \
    VerifyMailSerializer, ChangeEmailLoginSerializer, ConfirmChangeEmailLoginSerializer, CheckVerifyTokenSerializer, \
    ResendVerifyEmailSerializer
from gpt_base.auth.services import AuthService


@extend_schema(
    methods=['POST'],
    tags=['auth'],
    request=ForgotPasswordSerializer,
    description='forgot password',
    responses={200: {}}
)
@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def forgot_password(request):
    auth_service = AuthService()
    data = auth_service.forgot_password(request.data)
    return Response(data=data)


@extend_schema(
    methods=['POST'],
    tags=['auth'],
    request=ResetPasswordSerializer,
    description='reset password',
    responses={200: {}}
)
@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def reset_password(request):
    auth_service = AuthService()
    data = auth_service.reset_password(request.data)
    return Response(data=data)


@extend_schema(
    methods=['PUT'],
    tags=['auth'],
    request=ChangePasswordSerializer,
    description='change password',
    responses={200: {}}
)
@api_view(["PUT"])
@permission_classes([IsUserAuthenticated])
def change_password(request):
    auth_service = AuthService()
    data = auth_service.change_password(request.user, request.data)
    return Response(data=data)


@extend_schema(
    methods=['GET'],
    tags=['auth'],
    description='get me',
    responses={200: {}}
)
@api_view(["GET"])
@permission_classes([IsUserAuthenticated])
def get_me(request):
    auth_service = AuthService()
    data = auth_service.get_me(request.user)
    return Response(data=data)


@extend_schema(
    methods=['POST'],
    tags=['auth'],
    request=VerifyMailSerializer,
    description='verify email',
    responses={200: {}}
)
@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def verify_email(request):
    auth_service = AuthService()
    data = auth_service.verify_mail(request.data)
    return Response(data=data)


@extend_schema(
    methods=['POST'],
    tags=['auth'],
    request=ResendVerifyEmailSerializer,
    description='Resend verify email',
    responses={200: {}}
)
@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
def resend_verify_email(request):
    auth_service = AuthService()
    data = auth_service.resend_verify_email(request.data)
    return Response(data=data)


@extend_schema(
    methods=['PUT'],
    tags=['auth'],
    request=ChangeEmailLoginSerializer,
    description='change email login',
    responses={200: {}}
)
@api_view(["PUT"])
@permission_classes([IsUserAuthenticated])
def change_email_login(request):
    auth_service = AuthService()
    auth_service.change_email_login(request.user, request.data)
    return Response(data={})


@extend_schema(
    methods=['POST'],
    tags=['auth'],
    request=ConfirmChangeEmailLoginSerializer,
    description='confirm change email login',
    responses={200: {}}
)
@api_view(["POST"])
@permission_classes([AllowAny])
def confirm_change_email_login(request):
    auth_service = AuthService()
    data = auth_service.confirm_change_mail_login(request.data)
    return Response(data=data)


@extend_schema(
    methods=['POST'],
    tags=['auth'],
    request=CheckVerifyTokenSerializer,
    description='Check verify token valid or not',
    responses={204: None}
)
@api_view(["POST"])
@permission_classes([AllowAny])
def check_verify_token(request):
    auth_service = AuthService()
    auth_service.check_verify_token(request.data)
    return Response(status=status.HTTP_200_OK, data=dict(message="ok"))

@api_view(["POST"])
@permission_classes([AllowAny])
def check_session(request):
    return Response(status=status.HTTP_200_OK, data={
        "data": {
            "auth": True,
            "model": "ChatGPTAPI"
        },
        "message": "",
        "status": "Success",
    })
