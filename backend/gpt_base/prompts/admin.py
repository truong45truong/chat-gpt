from django.contrib import admin
from gpt_base.prompts.models import Prompts

# Register your models here.

class PromptsAdmin(admin.ModelAdmin):
    model = Prompts
    list_display = ['id', 'title', 'description' , 'created_at','updated_at']
admin.site.register(Prompts, PromptsAdmin)