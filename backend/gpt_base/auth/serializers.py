import logging

from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.state import token_backend
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from gpt_base import settings
# base constants
from gpt_base.common.constants import message_code
from gpt_base.common.constants.constant import RegexPattern, TokenObtainPairEnum
from gpt_base.common.constants.db_fields import DBFieldsCommon
# base utils
from gpt_base.common.utils.crypto import FieldCrypto
from gpt_base.common.utils.exceptions import CustomAPIException
from gpt_base.common.utils.middleware import get_current_user
from gpt_base.common.utils.strings import check_regex, get_current_time
# Models
from gpt_base.user.models import User

TokenGenerator = PasswordResetTokenGenerator()
crypto = FieldCrypto(settings.EMAIL_CRYPTO_FIELD_KEY)
logger = logging.getLogger(__name__)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Customizes JWT default Serializer to add more information about user"""

    def get_token(self, user, created_at=None):
        token = super().get_token(user)
        token[TokenObtainPairEnum.CREATED_AT_LABEL.value] = created_at
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        created_at = str(get_current_time())
        refresh = self.get_token(self.user, created_at)
        data = {
            "data": {
                "refresh": str(refresh),
                "access": str(refresh.access_token)  
            },
            "message": "",
            "status": "",
        }
        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """
    Inherit from `TokenRefreshSerializer` and touch the database
    before re-issuing a new access token and ensure that the user
    exists and is active.
    """

    def validate(self, attrs):
        token = token_backend.decode(attrs['refresh'])
        try:
            user = User.objects.exclude(delete_flag=True).get(pk=token['user_id'])
        except user.DoesNotExist:
            raise CustomAPIException(detail=message_code.THE_USER_HAD_BEEN_DELETED_FROM_THE_SYSTEM)

        return super().validate(attrs)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


    def validate_password(self, password):

        if not check_regex(RegexPattern.PASS_REGEX.value, password):
            raise CustomAPIException(detail="invalid password")

        return password


class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    old_password = serializers.CharField(required=True)

    def validate_new_password(self, new_password):
        user = self.context.get(DBFieldsCommon.USER.value)

        if not check_regex(RegexPattern.PASS_REGEX.value, new_password):
            raise CustomAPIException(detail="Invalid new password")

        if new_password == user.email:
            raise CustomAPIException(detail="Cannot matches password and email")

        return new_password

    def validate_old_password(self, old_password):
        user = self.context.get(DBFieldsCommon.USER.value)

        if not user.check_password(old_password):
            raise CustomAPIException(detail=message_code.DONT_MATCH_CURRENT_PASSWORD_PLEASE_CHECK_AGAIN)

        return old_password

    def update(self, instance, validated_data):
        instance.password = make_password(validated_data.get(DBFieldsCommon.NEW_PASSWORD.value))
        instance.save()
        return instance


class VerifyMailSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    email = serializers.CharField(required=True)


class ChangeEmailLoginSerializer(serializers.Serializer):
    new_email = serializers.EmailField(required=True)

    def validate_new_email(self, new_email):
        user = get_current_user()
        if user.email == new_email:
            raise CustomAPIException(detail=message_code.I_CANNOT_CHANGE_TO_EMAIL_ADDRESS_I_AM_USING)

        user = User.objects.filter(email=new_email).first()
        if user:
            raise CustomAPIException(detail="Email already exists")

        return new_email


class ConfirmChangeEmailLoginSerializer(serializers.Serializer):
    current_email = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    def validate(self, attrs):
        current_email = crypto.decrypt(attrs.get("current_email"))
        token = attrs.get("token")
        user_model = User
        try:
            user = user_model.objects.filter(email=current_email).first()
            if not TokenGenerator.check_token(user, token):
                raise CustomAPIException(detail=message_code.THIS_URL_IS_INVALID)

            if user.new_email is None:
                logger.info(f"No new mail exists")
                raise CustomAPIException(detail=message_code.FAILED_TO_CHANGE_EMAIL_ADDRESS)

            if user.email == user.new_email:
                logger.info(message_code.I_CANNOT_CHANGE_TO_EMAIL_ADDRESS_I_AM_USING)
                raise CustomAPIException(detail=message_code.FAILED_TO_CHANGE_EMAIL_ADDRESS)

            existing_user = user_model.objects.filter(email=user.new_email).first()
            if existing_user:
                logger.info("Email already in use")
                raise CustomAPIException(detail=message_code.FAILED_TO_CHANGE_EMAIL_ADDRESS)

            attrs['user'] = user
            return attrs
        except user_model.DoesNotExist:
            logger.info(message_code.PROVIDERS_HAVE_TO_BE_CUSTOMER_OR_CLIENT)
            raise CustomAPIException(detail=message_code.FAILED_TO_CHANGE_EMAIL_ADDRESS)


class CheckVerifyTokenSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    def validate(self, attrs):
        email = crypto.decrypt(attrs.get("email"))
        token = attrs.get("token")

        try:
            user_model = User
            user = user_model.objects.filter(email=email).first()
            if not TokenGenerator.check_token(user, token):
                raise CustomAPIException(detail=message_code.THIS_TOKEN_IS_INVALID)

        except user_model.DoesNotExist:
            raise CustomAPIException(detail=message_code.PROVIDERS_HAVE_TO_BE_CUSTOMER_OR_CLIENT)

        return attrs


class ResendVerifyEmailSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
