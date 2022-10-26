from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from embed_video.admin import AdminVideoMixin
# Register your models here.


@admin.register(Programme)
class ProgrammeAdmin(ImportExportModelAdmin):
    list_display = ('name','faculty', 'department')
    list_filter = ('faculty', 'department')
    search_fields = ['name','faculty', 'department']

@admin.register(Post)
class PostAdmin(ImportExportModelAdmin):
    list_display = ('title', 'department', 'site')
    list_filter = ('site',)

@admin.register(Faculty)
class FacultyAdmin(ImportExportModelAdmin):
    list_display = ('name',)

@admin.register(Department)
class DepartmentAdmin(ImportExportModelAdmin):
    list_display = ('name',)

@admin.register(Video)
class VideoAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass


admin.site.site_header = "Tech-U Career Update Administration Dashboard"