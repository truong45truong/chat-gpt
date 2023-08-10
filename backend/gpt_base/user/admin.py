
from django.contrib import admin
from gpt_base.user.models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ['id', 'email', 'first_name', 'last_name', 'is_verified_mail', 'is_active', 'is_superuser', 'is_staff', 'date_joined']
admin.site.register(User, UserAdmin)
