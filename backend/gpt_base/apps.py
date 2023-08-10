import decimal
import inspect

from django.apps import AppConfig


class BaseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gpt_base'

    def ready(self):
        for name in inspect.signature(decimal.Context).parameters:
            if name == 'prec':
                setattr(decimal.DefaultContext, name, 65)

        decimal.setcontext(decimal.DefaultContext)