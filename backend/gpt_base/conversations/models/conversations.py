from django.db import models

from gpt_base.common.constants.app_label import ModelAppLabel
from gpt_base.common.constants.db_table import DBTable
from gpt_base.common.constants.related_name import RelatedName
from gpt_base.common.constants.verbose_name_plural import VerboseNamePlural
from gpt_base.common.constants.constant import RoleEnum
from gpt_base.common.models.base import DateTimeModel
from gpt_base.members.models.members import Members
from gpt_base.master.models import TranslateTypesMaster


class Conversations(DateTimeModel):
    member = models.ForeignKey(Members, related_name=RelatedName.MEMBERS_CONVERSATIONS.value, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = DBTable.CONVERSATIONS.value
        app_label = ModelAppLabel.CONVERSATIONS.value
        verbose_name_plural = VerboseNamePlural.CONVERSATIONS.value

class Chat(DateTimeModel):
    conversation = models.ForeignKey(Conversations, related_name=RelatedName.CONVERSATIONS_CHATS.value, on_delete=models.CASCADE)
    prompt = models.TextField(blank=True)
    content = models.TextField(blank=True)
    content_translate = models.TextField(blank=True)
    translate_type = models.ForeignKey(TranslateTypesMaster, on_delete=models.CASCADE, null=True)
    role = models.CharField(default=RoleEnum.USER.value, max_length=100)
    name = models.CharField(max_length=100, blank=True)
    
    class Meta:
        db_table = DBTable.CHATS.value

