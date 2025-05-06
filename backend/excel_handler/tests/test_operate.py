import io
import pandas as pd
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class OperateExcelTestCase(APITestCase):
    def setUp(self):
        df = pd.DataFrame({"Price": [100, 200], "Tax": [10, 20]})
        buffer = io.BytesIO()
        df.to_excel(buffer, index=False)
        buffer.seek(0)
        response = self.client.post(reverse("upload_excel"), {"file": buffer}, format="multipart")
        self.session_id = response.data["data"]["session_id"]

    def test_add_column(self):
        payload = {
            "session_id": self.session_id,
            "operation": "add_column",
            "new_column": "Total",
            "expression": "Total = Price + Tax"
        }
        response = self.client.post(reverse("operate_excel"), data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Total", response.data["data"][0])