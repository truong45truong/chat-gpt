import logging

from django.utils.translation import gettext_lazy as _

from gpt_base.members.models import Members
logger = logging.getLogger(__name__)


class MembersBaseService:

    @staticmethod
    def get_member_by_id(user_id):
        logger.debug('Service: get_member_by_id called.')
        logger.debug('Service: get_member_by_id called with user id: %s.', user_id)

        try:
            user = Members.objects.get(user_id=user_id)
            logger.debug('Service: get_member_by_id called success.')
            return user
        except Members.DoesNotExist:
            return None

