import json
import operator
from datetime import datetime
from functools import reduce
from typing import Any

from rest_framework.test import APIClient, APITestCase


class LoggingAPIClient(APIClient):
    def generic(self, method, path, *args, **kwargs):
        if len(path) < 50:
            print(f"[{datetime.now()}] {method:<5} {path:<40}", end="")
            cut = 50
        else:
            print(f"[{datetime.now()}] {method:<5} {path} => \\\n      ", end="")
            cut = 150
        resp = super(LoggingAPIClient, self).generic(method, path, *args, **kwargs)
        try:
            data = resp.json()
        except:
            data = resp.content
        data = json.dumps(data, ensure_ascii=False, sort_keys=True, default=str)
        print(f" => {resp.status_code} {data[:cut]}{'...' if len(data) > cut else ''}")
        return resp


def get_by_dict_path(data: dict, path):
    return reduce(operator.getitem, path.split('.'), data)


class APITestCaseEx(APITestCase):
    client_class = LoggingAPIClient

    def assertResp(self, resp):
        self.assertEqual(resp.status_code // 100, 2, resp.content.decode())
        try:
            return resp.json()
        except:
            return resp.content.decode()

    def assertWrongResp(self, resp, code=None):
        if code is None:
            self.assertNotEqual(resp.status_code // 100, 2, resp.content.decode())
        else:
            self.assertEqual(resp.status_code, code, resp.content.decode())

        try:
            data = resp.json()
        except:
            return resp.content.decode()
        return data

    def assertBulk(self, data: list, path: str, value: Any):
        return all(get_by_dict_path(item, path) == value for item in data)


TEST_SETTINGS = dict(
    MIDDLEWARE=[
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'core.middleware.UTF8Middleware'
    ],
    INSTALLED_APPS=[
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',

        'rest_framework',
        'rest_framework.authtoken',

        'core',
        'questions'
    ],
    CACHES={
        "default": {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'tests_online_cache',
        }
    }

)
