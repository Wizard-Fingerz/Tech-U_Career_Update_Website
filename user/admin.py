from django.contrib import admin
from .models import *
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email')
    list_filter = ('is_admin', 'is_student', 'is_moderator')
    search_fields = ['username', 'first_name', 'last_name']


admin.site.register(User, UserAdmin)

admin.site.register([Profile, Comment])
