import io
import pandas as pd
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from openpyxl import load_workbook



class ExportExcelTestCase(APITestCase):
    def setUp(self):
        df = pd.DataFrame({"Product": ["X", "Y"], "Price": [10, 20]})
        buffer = io.BytesIO()
        df.to_excel(buffer, index=False)
        buffer.seek(0)
        buffer.name = "test_file.xlsx"  # Required by Django for multipart

        upload_url = reverse("upload_excel")
        response = self.client.post(upload_url, {"file": buffer}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.session_id = response.data["data"]["session_id"]

    def test_export_excel(self):
        url = reverse("export_excel") + f"?session_id={self.session_id}"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Read streamed content into memory
        content = b"".join(response.streaming_content)

        # Check for Excel binary signature (ZIP)
        self.assertTrue(content.startswith(b'PK'))
        self.assertGreater(len(content), 100)

        # Optional: Parse content as Excel
        buffer = io.BytesIO(content)
        df = pd.read_excel(buffer)

        self.assertListEqual(list(df.columns), ["Product", "Price"])
        self.assertEqual(df.iloc[0]["Product"], "X")
        self.assertEqual(df.iloc[1]["Price"], 20)
