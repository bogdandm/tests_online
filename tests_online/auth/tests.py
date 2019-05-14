import hashlib
import uuid

from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse

from core.tests.utils import APITestCaseEx, TEST_SETTINGS
from .test_utils import get_auth_headers


@override_settings(**TEST_SETTINGS)
class UserApi(APITestCaseEx):
    CREDENTIALS = {"username": "user", "password": hashlib.sha256(uuid.uuid4().bytes).hexdigest()}

    def test_user_info(self):
        User = get_user_model()
        user = User.objects.create_superuser(**self.CREDENTIALS, email='')

        resp = self.client.get(reverse('user-info'))
        self.assertWrongResp(resp, 401)

        headers = get_auth_headers(self.client, **self.CREDENTIALS)
        resp = self.client.get(reverse('user-info'), **headers)
        self.assertResp(resp)

    def test_signup(self):
        resp = self.client.post(reverse('user-signup'), data=self.CREDENTIALS)
        self.assertResp(resp)

        headers = get_auth_headers(self.client, **self.CREDENTIALS)
        resp = self.client.get(reverse('user-info'), **headers)
        self.assertResp(resp)