from random import randint

from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse

from auth.test_utils import get_auth_headers
from core.tests import random_text
from core.tests.utils import APITestCaseEx


@override_settings(
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
    ]
)
class TestReadApi(APITestCaseEx):
    CREDENTIALS_ADMIN = {
        "username": "test_admin",
        "email": "",
        "password": "qwerty12"
    }
    CREDENTIALS = {
        "username": "test_user",
        "email": "",
        "password": "qwerty12"
    }

    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.user = cls.User.objects.create_user(**cls.CREDENTIALS)
        cls.admin = cls.User.objects.create_superuser(**cls.CREDENTIALS_ADMIN)

    def get_test_payload(self, is_private=False, params=None, stats_restriction="off"):
        data = {
            "title": random_text.random_sentences(3, 1)[:-1],
            "description": random_text.random_paragraph((20, 30), (3, 7)),
            "is_private": is_private,
            "stats_restriction": stats_restriction,
            "questions": [
                {
                    "position": i + 1,
                    "text": random_text.random_paragraph((20, 30), (3, 7)),
                    "answers": [
                        {
                            "position": j + 1,
                            "text": random_text.random_paragraph((20, 30), (1, 2)),
                            "params_value": [0] if params is None else [randint(0, 3) for _ in range(params)]
                        }
                        for j in range(randint(2, 10))
                    ]
                }
                for i in range(randint(10, 100))
            ]
        }

        if params is not None:
            data["params"] = [random_text.random_word().upper() for _ in range(params)]
            data["params_defaults"] = [randint(0, 5) for _ in range(params)]

        return data

    def test_create(self):
        payload = self.get_test_payload(is_private=True)
        headers = get_auth_headers(self.client, **self.CREDENTIALS)

        resp = self.client.post(reverse('tests-list'), data=payload)
        self.assertWrongResp(resp, 401)

        resp = self.client.post(reverse('tests-list'), data=payload, **headers)
        test = self.assertResp(resp)
        self.assertEqual(len(payload["questions"]), len(test["questions"]))
        self.assertEqual(len(payload["questions"][0]["answers"]), len(test["questions"][0]["answers"]))

        resp = self.client.get(reverse('tests-list'))
        tests1 = self.assertResp(resp)
        resp = self.client.get(reverse('tests-list'), **headers)
        tests2 = self.assertResp(resp)
        self.assertEqual(tests2["count"] - tests1["count"], 1)
        self.assertTrue(test["id"] in {t["id"] for t in tests2["results"]})

    # def test_update(self):
    #     payload = self.get_test_payload(is_private=True)
    #     headers = get_auth_headers(self.client, **self.CREDENTIALS)
    #     headers_admin = get_auth_headers(self.client, **self.CREDENTIALS_ADMIN)
    #
    #     resp = self.client.post(reverse('tests-list'), data=payload, **headers)
    #     test = self.assertResp(resp)
    #     test_hash = test["hash"]
    #
    #
