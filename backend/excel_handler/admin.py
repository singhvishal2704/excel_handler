from django.contrib import admin
from excel_handler.models import ExcelFile, ExcelVersion, ExcelOperationLog


class BaseAdmin(admin.ModelAdmin):
    list_per_page = 25  # Pagination
    list_filter = ('is_active', 'created_at', 'updated_at') 
    search_fields = ('id',)  # Default search
    ordering = ('-created_at',)

    def get_list_display(self, request):
        # Dynamically show all model fields
        return [field.name for field in self.model._meta.fields]


@admin.register(ExcelFile)
class ExcelFileAdmin(BaseAdmin):
    def get_queryset(self, request):
        return ExcelFile.all_objects.all()

@admin.register(ExcelVersion)
class ExcelVersionAdmin(BaseAdmin):
    def get_queryset(self, request):
        return ExcelVersion.all_objects.all()

@admin.register(ExcelOperationLog)
class ExcelOperationLogAdmin(BaseAdmin):
    def get_queryset(self, request):
        return ExcelOperationLog.all_objects.all()
