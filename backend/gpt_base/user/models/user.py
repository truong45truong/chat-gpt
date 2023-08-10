from django.db import models

from gpt_base.common.constants.app_label import ModelAppLabel
from gpt_base.common.constants.db_fields import DBUserFields
from gpt_base.common.constants.db_table import DBTable
from gpt_base.common.constants.related_name import RelatedName
from gpt_base.common.constants.verbose_name_plural import VerboseNamePlural
from gpt_base.common.models.base import CustomBaseUserModel

class User(CustomBaseUserModel):
    first_name = models.CharField(('first name'), max_length=30, null=True, blank=True)
    last_name = models.CharField(('last name'), max_length=150, null=True, blank=True)
    new_email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    email_updated_date = models.DateTimeField(null=True, blank=True)
    is_verified_mail = models.BooleanField(default=False)
    is_receive_mail = models.BooleanField(default=False)
    delete_flag = models.BooleanField(default=False)
    
    class Meta:
        db_table = DBTable.USER.value
        app_label = ModelAppLabel.USER.value
        verbose_name_plural = VerboseNamePlural.USER.value
        indexes = [
            models.Index(fields=[
                DBUserFields.FIRST_NAME.value,
                DBUserFields.LAST_NAME.value,
            ])
        ]
