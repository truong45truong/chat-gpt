import logging

from django.db import transaction
from django.utils.translation import gettext_lazy as _

# from gpt_base.common.constants.mail import MailTemplateEnum
# from gpt_base.other.mail.services import MailService
from gpt_user.members.serializers.registration import RegisterMembersSerializer

logger = logging.getLogger(__name__)


class MemberRegistrationService:

    def __init__(self):
        super(MemberRegistrationService, self).__init__()
        # self._mail_service = MailService()


    def register_member(self, req_data):
        # logger.debug("Service: register member called. with data: %s", req_data)

        with transaction.atomic():
            serializers = RegisterMembersSerializer(data=req_data)
            serializers.is_valid(raise_exception=True)
            serializers.save()
            # member = serializers.save()
            # self._mail_service.send_mail_by_type(email_type_enum=MailTemplateEnum.NO_07, member=member)

            # logger.debug("Service: register member called success")

