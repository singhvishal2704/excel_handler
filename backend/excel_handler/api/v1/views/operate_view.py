from rest_framework.views import APIView
from rest_framework.response import Response
from excel_handler.services.dataframe_session import get_cached_dataframe, update_cached_dataframe
from excel_handler.services.operation_executor import add_column, filter_rows, combine_columns
from excel_handler.services.versioning import save_new_version, undo_last_operation
from excel_handler.services.gpt_expression_parser import prompt_to_pandas_expression
from common.response_utils import success_response, error_response
from common.logging_utils import logger
import re

class OperateOnExcelView(APIView):
    def post(self, request):
        try:
            self.payload = request.data
            self.session_id = self.payload.get("session_id")

            # Undo operation handler
            if self.payload.get("operation") == "undo":
                try:
                    df = undo_last_operation(self.session_id)
                except ValueError as ve:
                    return error_response(str(ve), status_code=400)

                update_cached_dataframe(self.session_id, df)
                return success_response(df.to_dict(orient="records"))

            df = self._get_dataframe()
            if isinstance(df, dict):
                return error_response(**df)

            updated_df = self._apply_operation(df)
            update_cached_dataframe(self.session_id, updated_df)
            save_new_version(self.session_id, updated_df, self.payload.get("operation"), self.payload.get("description", ""))

            return success_response(updated_df.to_dict(orient="records"))
        except ValueError as ve:
            return error_response(str(ve), status_code=400)
        except Exception as e:
            logger.exception("Error in OperateOnExcelView")
            return error_response(str(e), status_code=500)

    def _get_dataframe(self):
        if not self.session_id:
            return {"message": "Missing session_id", "status_code": 400}
        df = get_cached_dataframe(self.session_id)
        if df is None:
            return {"message": "Session not found or expired", "status_code": 404}
        return df

    def _extract_code_snippet(self, content):
        # Use regex to extract code between triple backticks or fallback to full content
        match = re.search(r"```(?:python)?\n?(.*?)```", content, re.DOTALL)
        return match.group(1).strip() if match else content.strip()

    def _apply_operation(self, df):
        op = self.payload.get("operation")

        if op == "add_column":
            new_column = self.payload["new_column"]
            prompt = self.payload["expression"]  # This is a natural language instruction

            try:
                expression_code = prompt_to_pandas_expression(prompt, df.columns.tolist())
                expression_code = self._extract_code_snippet(expression_code)
            except Exception as e:
                logger.exception("Groq expression parsing failed")
                raise ValueError("Unable to generate expression from prompt. Please rephrase your input.")

            local_context = {"df": df.copy()}
            try:
                exec(expression_code, {}, local_context)
            except Exception as e:
                logger.exception("Error evaluating generated expression code")
                raise ValueError("Failed to execute generated code. Please validate column names and logic.")

                        # Return any updated DataFrame object created by GPT
            for var in reversed(list(local_context.keys())):
                if isinstance(local_context[var], type(df)) and not var.startswith("_"):
                    return local_context[var]
            return local_context["df"]

        elif op == "filter_rows":
            prompt = self.payload["expression"]
            try:
                expression_code = prompt_to_pandas_expression(
                    f"You are working with a Pandas DataFrame named 'df'. Always use 'df' as the DataFrame variable in your expression. {prompt}", df.copy().columns.tolist())
                expression_code = self._extract_code_snippet(expression_code)
                if not re.match(r"^\s*df\s*=", expression_code):
                    expression_code = f"df = {expression_code}"
            except Exception as e:
                logger.exception("Groq expression parsing failed for filter_rows")
                raise ValueError("Unable to generate filter expression. Please rephrase your input.")

            local_context = {"df": df.copy()}
            try:
                exec(expression_code, {}, local_context)
            except Exception as e:
                logger.exception("Error executing filter expression")
                raise ValueError("Failed to execute filter code. Please recheck the logic.")

            return local_context["df"]

        elif op == "combine_columns":
            return combine_columns(df, self.payload["columns"], self.payload["new_column"], self.payload.get("separator", " "))

        raise ValueError("Unsupported operation")
