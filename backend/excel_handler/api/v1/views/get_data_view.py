from rest_framework.views import APIView
from excel_handler.services.dataframe_session import get_cached_dataframe
from common.response_utils import success_response, error_response
from common.logging_utils import logger

class GetExcelDataView(APIView):
    def get(self, request):
        try:
            session_id = request.query_params.get("session_id")
            if not session_id:
                return error_response("Missing session_id")

            df = get_cached_dataframe(session_id)
            if df is None:
                return error_response("Session not found or expired", status_code=404)

            return success_response(df.to_dict(orient="records"))
        except Exception as e:
            logger.exception("Error in GetExcelDataView")
            return error_response(str(e), status_code=500)
