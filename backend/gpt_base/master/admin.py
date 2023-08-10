
from django.contrib import admin
from gpt_base.master.models import TranslateTypesMaster

# Register your models here.

class TranslateTypesMasterAdmin(admin.ModelAdmin):
    model = TranslateTypesMaster
    list_display = ['id', 'name', 'delete_flag']
admin.site.register(TranslateTypesMaster, TranslateTypesMasterAdmin)
