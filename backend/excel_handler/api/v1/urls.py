from django.urls import path
from .views.upload_view import UploadExcelView
from .views.operate_view import OperateOnExcelView
from .views.get_data_view import GetExcelDataView
from .views.export_view import ExportExcelFileView

urlpatterns = [
    path('v1/upload/', UploadExcelView.as_view(), name='upload_excel'),
    path('v1/operate/', OperateOnExcelView.as_view(), name='operate_excel'),
    path('v1/get-data/', GetExcelDataView.as_view(), name='get_excel_data'),
    path('v1/export/', ExportExcelFileView.as_view(), name='export_excel'),
]
