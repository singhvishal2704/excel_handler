import uuid
import pandas as pd
from excel_handler.models import ExcelFile
from excel_handler.services.file_manager import read_excel_file
from common.storage_client import upload_file


def track_uploaded_file(file) -> tuple[str, pd.DataFrame]:
    """
    Saves file to local or S3, creates session_id, stores DB entry.
    Returns (session_id, DataFrame)
    """
    session_id = str(uuid.uuid4())
    df = read_excel_file(file)

    storage_path = upload_file(file, file.name)

    ExcelFile.objects.create(
        session_id=session_id,
        original_filename=file.name,
        upload_path=storage_path
    )

    return session_id, df
