
from django.contrib import admin
from gpt_base.members.models import Members

# Register your models here.

class MembersAdmin(admin.ModelAdmin):
    model = Members
    list_display = ['id', 'token_limit', 'quantity_token_used']
admin.site.register(Members, MembersAdmin)
