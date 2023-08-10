from django.contrib import admin
from gpt_base.documents.models import Templates, WorkBooks , Documents

# Register your models here.

class TemplatesAdmin(admin.ModelAdmin):
    model = Templates
    list_display = ['id', 'name']
admin.site.register(Templates , TemplatesAdmin)

class WorkBooksAdmin(admin.ModelAdmin):
    model = WorkBooks
    list_display = ['id', 'name']
admin.site.register(WorkBooks, WorkBooksAdmin)

class DocumentsAdmin(admin.ModelAdmin):
    model = Documents
    list_display = ['id', 'workbook_id']
admin.site.register(Documents, DocumentsAdmin)