import logging

from django.utils.translation import gettext_lazy as _

from gpt_base.user.models import User
logger = logging.getLogger(__name__)


class UserBaseService:

    @staticmethod
    def get_user_by_id(user_id):
        logger.debug('Service: get_user_by_id called.')
        logger.debug('Service: get_user_by_id called with user id: %s.', user_id)

        try:
            user = User.objects.get(id=user_id)
            logger.debug('Service: get_user_by_id called success.')
            return user
        except User.DoesNotExist:
            return None

