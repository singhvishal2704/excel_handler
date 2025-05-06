import io
import pandas as pd
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class UploadExcelTestCase(APITestCase):
    def test_upload_excel_file(self):
        df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
        buffer = io.BytesIO()
        df.to_excel(buffer, index=False)
        buffer.seek(0)

        response = self.client.post(reverse("upload_excel"), {"file": buffer}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("session_id", response.data["data"])
        

