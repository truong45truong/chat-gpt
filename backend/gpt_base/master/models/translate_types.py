from gpt_base.common.constants.app_label import ModelAppLabel
from gpt_base.common.constants.db_table import DBTable
from gpt_base.common.models.base import MaterBaseModel


class TranslateTypesMaster(MaterBaseModel):
    class Meta:
        db_table = DBTable.M_TRANSLATE_TYPES.value
        app_label = ModelAppLabel.MASTER.value
