import pandas as pd
from django.db import transaction
from excel_handler.models import ExcelFile, ExcelVersion, ExcelOperationLog
from common.logging_utils import logger


def save_new_version(session_id: str, df: pd.DataFrame, operation_type: str, description: str = "") -> None:
    try:
        with transaction.atomic():
            excel_file = ExcelFile.objects.get(session_id=session_id)

            # Get next version number
            last_version = ExcelVersion.all_objects.filter(file=excel_file).order_by('-version_number').first()
            next_version = (last_version.version_number + 1) if last_version else 1

            # Save new version
            version = ExcelVersion.objects.create(
                file=excel_file,
                version_number=next_version,
                dataframe_json=df.to_dict(orient="records"),
            )

            # Log operation
            ExcelOperationLog.objects.create(
                version=version,
                operation_type=operation_type,
                description=description or f"{operation_type} performed"
            )
    except Exception as e:
        logger.exception("Failed to save new version")
        raise


def get_latest_version(session_id: str) -> pd.DataFrame:
    try:
        excel_file = ExcelFile.objects.get(session_id=session_id)
        latest_version = excel_file.versions.first()
        if not latest_version:
            raise ValueError("No versions found for this file.")
        return pd.DataFrame(latest_version.dataframe_json)
    except Exception as e:
        logger.exception("Failed to retrieve latest version")
        raise


def undo_last_operation(session_id: str) -> pd.DataFrame:
    try:
        excel_file = ExcelFile.objects.get(session_id=session_id)
        latest_versions = list(excel_file.versions.all().order_by('-version_number'))

        if len(latest_versions) < 2:
            raise ValueError("No previous version available to undo.")

        # Delete latest version
        latest_versions[0].delete()

        # Return previous version
        previous_df = latest_versions[1].dataframe_json
        return pd.DataFrame(previous_df)
    except Exception as e:
        logger.exception("Undo operation failed")
        raise
