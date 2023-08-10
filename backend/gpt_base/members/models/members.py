from django.db import models

from gpt_base.common.constants.app_label import ModelAppLabel
from gpt_base.common.constants.db_table import DBTable
from gpt_base.common.constants.related_name import RelatedName
from gpt_base.common.constants.verbose_name_plural import VerboseNamePlural
from gpt_base.common.models.base import DateTimeModel
from gpt_base.user.models.user import User

class Members(DateTimeModel):
    user = models.OneToOneField(User, related_name=RelatedName.USER_MEMBERS.value, on_delete=models.RESTRICT, null=True)
    token_limit = models.IntegerField(default=100000)
    quantity_token_used = models.IntegerField(default=0)
    
    class Meta:
        db_table = DBTable.MEMBERS.value
        app_label = ModelAppLabel.MEMBERS.value
        verbose_name_plural = VerboseNamePlural.MEMBERS.value