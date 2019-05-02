import operator

from django.test import override_settings
from django.urls import reverse

from core.tests.utils import APITestCaseEx
from .data_setup import QuestionsTestData
from .. import models


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
class TestReadApi(QuestionsTestData, APITestCaseEx):
    def test_list(self):
        resp = self.client.get(reverse('tests-list'))
        tests = self.assertResp(resp)["results"]
        self.assertEqual(len(tests), 1)
        self.assertEqual(tests[0]["title"], "public_test")

        self.assertTrue(self.client.login(**self.CREDENTIALS))

        resp = self.client.get(reverse('tests-list'))
        tests = self.assertResp(resp)["results"]
        self.assertGreater(len(tests), 1)
        self.assertTrue("private_test" in map(operator.itemgetter('title'), tests))

    def test_retrieve(self):
        for h in models.Test.objects.values_list("hash", flat=True):
            resp = self.client.get(reverse('tests-detail', kwargs={'hash': h}))
            test = self.assertResp(resp)
            self.assertTrue(test["questions"])
            self.assertTrue(all(q["answers"] for q in test["questions"]))
