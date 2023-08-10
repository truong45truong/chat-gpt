import logging

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from gpt_base import settings
from gpt_base.auth.serializers import ResetPasswordSerializer, ForgotPasswordSerializer, ChangePasswordSerializer, \
    VerifyMailSerializer, ConfirmChangeEmailLoginSerializer, ChangeEmailLoginSerializer, CheckVerifyTokenSerializer, \
    ResendVerifyEmailSerializer
from gpt_base.common.constants import message_code
from gpt_base.common.constants.db_fields import DBFieldsCommon
from gpt_base.common.constants.mail import MailTemplateEnum
from gpt_base.common.constants.constant import ProviderEnum
from gpt_base.common.utils.crypto import FieldCrypto
from gpt_base.common.utils.exceptions import CustomAPIException
from gpt_base.common.utils.strings import get_current_time
# from gpt_base.other.mail.services import MailService
from gpt_base.user.serializers.user import UserInfoSerializer
from gpt_base.members.serializers.members import MembersDetailUpdateSerializer
# Models
from gpt_base.user.models import User
from gpt_base.members.models import Members


logger = logging.getLogger(__name__)
TokenGenerator = PasswordResetTokenGenerator()


class AuthService:

    def __init__(self):
        super(AuthService, self).__init__()
        # self._mail_service = MailService()
        self.__crypto = FieldCrypto(settings.EMAIL_CRYPTO_FIELD_KEY)

    # def forgot_password(self, req_data):
    #     logger.debug("Service: forgot password called. with data: %s", req_data)

    #     serializer = ForgotPasswordSerializer(data=req_data)
    #     serializer.is_valid(raise_exception=True)

    #     email = serializer.data[DBFieldsCommon.EMAIL.value]
    #     user = self.get_user(email)
    #     full_name = self.get_full_name_user(user)
    #     self._mail_service.send_mail_by_type(email_type_enum=MailTemplateEnum.NO_12, user=user, full_name=full_name)

    #     logger.debug("Service: forgot password called success")
    #     return dict(message=message_code.USER_FORGOT_PASSWORD_SUCCESS)

    # def reset_password(self, req_data):
    #     logger.debug("Service: reset password called. with data: %s", req_data)

    #     serializer = ResetPasswordSerializer(data=req_data)
    #     serializer.is_valid(raise_exception=True)

    #     email = self.__crypto.decrypt(serializer.data[DBFieldsCommon.EMAIL.value])
    #     token = serializer.data[DBFieldsCommon.TOKEN.value]
    #     password = serializer.data[DBFieldsCommon.PASSWORD.value]

    #     user = self.get_user(email)

    #     if TokenGenerator.check_token(user, token):
    #         user.set_password(password)
    #         user.save()
    #     else:
    #         raise CustomAPIException(detail=message_code.THIS_URL_IS_INVALID)

    #     full_name = self.get_full_name_user(user)
    #     self._mail_service.send_mail_by_type(email_type_enum=MailTemplateEnum.NO_13, user=user, full_name=full_name)

    #     logger.debug("Service: reset password called success")
    #     return dict(message=message_code.RESET_PASSWORD_SUCCESS)

    def change_password(self, user, req_data):
        logger.debug("Service: change password called. with data: %s", req_data)

        serializer = ChangePasswordSerializer(data=req_data, context=dict(user=user))
        serializer.is_valid(raise_exception=True)
        serializer.update(user, req_data)

        logger.debug("Service: change password called success")
        return dict(message=message_code.CHANGE_PASSWORD_SUCCESS)

    def get_user(self, email):
        user_model = User

        try:
            user = user_model.objects.get(email=email)

            return user
        except user_model.DoesNotExist:
            raise CustomAPIException(detail=message_code.THIS_EMAIL_NOT_YET_REGISTER)

    def get_me(self, user):
        logger.debug("Service: get me called. with user: %s", user)

        member = Members.objects.get(user=user)
        res_data = MembersDetailUpdateSerializer(member)

        logger.debug("Service: get me called success")
        return {
            "data": res_data.data
        }

    # def verify_mail(self, req_data):
    #     logger.debug("Service: verify mail called. with data: %s", req_data)

    #     serializer = VerifyMailSerializer(data=req_data)
    #     serializer.is_valid(raise_exception=True)
    #     token = serializer.data[DBFieldsCommon.TOKEN.value]

    #     auth_service = AuthService()
    #     user = auth_service.get_user(
    #         self.__crypto.decrypt(serializer.data.get(DBFieldsCommon.EMAIL.value, None)),
    #         serializer.data.get(ProviderEnum.PROVIDER_LABEL.value, None)
    #     )

    #     if TokenGenerator.check_token(user, token):

    #         if user.is_verified_mail:
    #             raise CustomAPIException(detail=message_code.THIS_URL_IS_INVALID)

    #         user.is_verified_mail = True
    #         user.save()
    #         return dict(message=message_code.VERIFY_MAIL_SUCCESS)
    #     else:
    #         raise CustomAPIException(detail=message_code.THIS_URL_IS_INVALID)

    # def resend_verify_email(self, req_data):
    #     logger.debug("Service: Resend verify email called. with data: %s", req_data)

    #     serializer = ResendVerifyEmailSerializer(data=req_data)
    #     serializer.is_valid(raise_exception=True)

    #     provider = serializer.data.get("provider")
    #     if provider not in [ProviderEnum.CLIENT.value, ProviderEnum.CUSTOMER.value]:
    #         raise CustomAPIException(detail=_('This feature just support for Client & Customer'))

    #     user_model = User
    #     try:
    #         user = user_model.objects.get(email=serializer.data.get("email"))
    #         if user.is_verified_mail:
    #             raise CustomAPIException(detail=message_code.THIS_EMAIL_VERIFIED)
    #     except user_model.DoesNotExist:
    #         raise CustomAPIException(detail=message_code.THIS_EMAIL_NOT_YET_REGISTER)

    #     self._mail_service.send_mail_by_type(email_type_enum=MailTemplateEnum.NO_07, client=user)

        return dict(message=message_code.RESEND_VERIFY_MAIL_SUCCESS)

    def get_full_name_user(self, user):
        full_name = f'{user.first_name} {user.last_name}'
        return full_name

    # def change_email_login(self, user, req_data):
    #     logger.debug("Service: change email login called. with data: %s", req_data)

    #     with transaction.atomic():
    #         serializer = ChangeEmailLoginSerializer(data=req_data)
    #         serializer.is_valid(raise_exception=True)
    #         new_email = serializer.data.get("new_email")
    #         user.new_email = new_email
    #         user.save()
    #         self._mail_service.send_mail_by_type(email_type_enum=MailTemplateEnum.NO_11, user=user, new_email=new_email)
    #         logger.info("Service: change email login called success")

    # def confirm_change_mail_login(self, req_data):
    #     logger.debug("Service: confirm change email login called. with data: %s", req_data)

    #     with transaction.atomic():
    #         serializer = ConfirmChangeEmailLoginSerializer(data=req_data)
    #         serializer.is_valid(raise_exception=True)
    #         user = serializer.validated_data.get('user')
    #         user.email = user.new_email
    #         user.new_email = None
    #         user.email_updated_date = get_current_time()
    #         user.save()

    #         logger.info("Service: confirm change email login called success")
    #         return dict(message=message_code.YOU_HAVE_SUCCESSFULLY_CHANGED_YOUR_EMAIL_ADDRESS)

    # def check_verify_token(self, req_data):
    #     logger.debug("Service: check verify token is valid or not. with data: %s", req_data)
    #     serializer = CheckVerifyTokenSerializer(data=req_data)
    #     serializer.is_valid(raise_exception=True)