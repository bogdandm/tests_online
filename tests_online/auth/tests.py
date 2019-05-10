from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse

from core.tests.utils import APITestCaseEx, TEST_SETTINGS
from .test_utils import get_auth_headers


@override_settings(**TEST_SETTINGS)
class TestReadApi(APITestCaseEx):
    CREDENTIALS = {"username": "user", "password": "qwerty12"}

    def test_current_user(self):
        User = get_user_model()
        user = User.objects.create_superuser(**self.CREDENTIALS, email='')

        resp = self.client.get(reverse('current_user'))
        self.assertWrongResp(resp, 401)

        headers = get_auth_headers(self.client, **self.CREDENTIALS)
        resp = self.client.get(reverse('current_user'), **headers)
        self.assertResp(resp)
