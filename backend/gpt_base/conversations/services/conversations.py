import logging

from django.utils.translation import gettext_lazy as _

from gpt_base.conversations.models import Conversations
logger = logging.getLogger(__name__)


class ConversationsBaseService:

    @staticmethod
    def init():
        pass

