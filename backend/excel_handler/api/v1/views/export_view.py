# excel_handler/api/v1/views/export_view.py
from rest_framework.views import APIView
from django.http import FileResponse
from excel_handler.services.dataframe_session import get_cached_dataframe
from excel_handler.services.versioning import get_latest_version
from excel_handler.services.file_manager import write_excel_to_memory
from common.response_utils import error_response
from common.logging_utils import logger

class ExportExcelFileView(APIView):
    def get(self, request):
        try:
            session_id = request.query_params.get("session_id")
            if not session_id:
                return error_response("Missing session_id")

            df = get_cached_dataframe(session_id)
            if df is None:
                df = get_latest_version(session_id)

            excel_file = write_excel_to_memory(df)
            return FileResponse(excel_file, as_attachment=True, filename="processed_data.xlsx")
        except Exception as e:
            logger.exception("Error in ExportExcelFileView")
            return error_response(str(e), status_code=500)