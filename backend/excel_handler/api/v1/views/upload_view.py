import uuid
from rest_framework.views import APIView
from excel_handler.serializers.upload_serializer import ExcelUploadSerializer
from excel_handler.services.file_manager import read_excel_file
from excel_handler.services.dataframe_session import cache_dataframe
from excel_handler.services.versioning import save_new_version
from excel_handler.services.file_tracker import track_uploaded_file
from common.response_utils import success_response, error_response
from common.logging_utils import logger

class UploadExcelView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.serializer_class = ExcelUploadSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return error_response(serializer.errors, status_code=400)

            file = serializer.validated_data['file']
            session_id, df = track_uploaded_file(file)

            # Cache the uploaded DataFrame
            cache_dataframe(session_id, df)

            # Save Version 1 in DB
            save_new_version(session_id, df, operation_type="initial_upload", description="File uploaded")

            return success_response({
                "session_id": session_id,
                "columns": df.columns.tolist()
            })
        except Exception as e:
            logger.exception("Error in UploadExcelView")
            return error_response(str(e), status_code=500)
