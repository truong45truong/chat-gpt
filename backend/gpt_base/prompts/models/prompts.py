from django.db import models

from gpt_base.common.constants.app_label import ModelAppLabel
from gpt_base.common.constants.db_table import DBTable
from gpt_base.common.constants.related_name import RelatedName
from gpt_base.common.constants.verbose_name_plural import VerboseNamePlural
from gpt_base.common.models.base import DateTimeModel
from gpt_base.members.models.members import Members

class Prompts(DateTimeModel):
    member = models.ForeignKey(Members, related_name=RelatedName.MEMBERS_PROMPTS.value, on_delete=models.CASCADE)
    title = models.CharField(max_length = 256)
    description = models.TextField()

    class Meta:
        db_table = DBTable.PROMPTS.value
        app_label = ModelAppLabel.PROMPTS.value
        verbose_name_plural = VerboseNamePlural.PROMPTS.value