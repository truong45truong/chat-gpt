import logging

from django.utils.translation import gettext_lazy as _

from gpt_base.conversations.models import Chat
logger = logging.getLogger(__name__)


class ChatBaseService:

    @staticmethod
    def init():
        pass

