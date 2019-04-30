import json
from datetime import datetime

from rest_framework.test import APIClient, APITestCase


class LoggingAPIClient(APIClient):
    def generic(self, method, path, *args, **kwargs):
        print(f"[{datetime.now()}] {method:<5} {path:<40}", end="")
        resp = super(LoggingAPIClient, self).generic(method, path, *args, **kwargs)
        try:
            data = resp.json()
        except:
            data = resp.content
        data = json.dumps(data, ensure_ascii=False, sort_keys=True)
        print(f" => {resp.status_code} {data[:50]}{'...' if len(data) > 50 else ''}")
        return resp


class APITestCaseEx(APITestCase):
    credentials = {"username": "admin", "password": "asdfGDFHdsfhadfhHSER"}
    auto_login = False
    client_class = LoggingAPIClient

    def assertResp(self, resp):
        self.assertEqual(resp.status_code // 100, 2, resp.content)
        try:
            data = resp.json()
        except Exception as e:
            raise e
        return data

    def setUp(self):
        if self.auto_login:
            self.client.login(**self.credentials)
