from django.db import models

from gpt_base.common.constants.app_label import ModelAppLabel
from gpt_base.common.constants.db_table import DBTable
from gpt_base.common.constants.related_name import RelatedName
from gpt_base.common.constants.verbose_name_plural import VerboseNamePlural
from gpt_base.common.models.base import DateTimeModel
from gpt_base.members.models.members import Members

class Templates(DateTimeModel):
    name = models.CharField(max_length = 255)
    params = models.TextField()
    html = models.TextField()
    content = models.CharField(max_length = 2555 , null = True)
    text_feature_button = models.CharField(max_length = 255, null = True)
    icon = models.CharField(max_length = 255 , null = True)
    question_asked = models.TextField(null = True)
    class Meta:
        db_table = DBTable.TEMPLATES.value

class WorkBooks(DateTimeModel):
    name = models.CharField(max_length = 255)
    quantity_document = models.IntegerField(default=0)
    member = models.ForeignKey(Members, related_name=RelatedName.WORKBOOKS_MEMBERS.value, on_delete=models.CASCADE)

    class Meta:
        db_table = DBTable.WORK_BOOKS.value

class Documents(DateTimeModel):
    content = models.TextField()
    params_value = models.TextField()
    workbook = models.ForeignKey(WorkBooks, related_name=RelatedName.DOCUMENTS_WORKBOOK.value, on_delete=models.CASCADE)
    template = models.ForeignKey(Templates, related_name=RelatedName.DOCUMENTS_TEMPLATES.value, on_delete=models.CASCADE)
    member = models.ForeignKey(Members, null= True, related_name=RelatedName.DOCUMENTS_MEMBERS.value, on_delete=models.CASCADE)
    name = models.CharField(max_length = 255 , null = True)
    language = models.CharField(max_length = 255 )
    class Meta:
        db_table = DBTable.DOCUMENTS.value
        app_label = ModelAppLabel.DOCUMENTS.value
        verbose_name_plural = VerboseNamePlural.DOCUMENTS.value