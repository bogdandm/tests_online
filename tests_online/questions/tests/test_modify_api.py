from random import choice, randint

from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse

from auth.test_utils import get_auth_headers
from core.tests import random_text
from core.tests.utils import APITestCaseEx, TEST_SETTINGS
from .data_setup import QuestionsTestData
from .. import models


def get_test_payload(is_private=False, params=None, stats_restriction="off"):
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


@override_settings(**TEST_SETTINGS)
class TestModifyApi(APITestCaseEx):
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

    def test_create(self):
        payload = get_test_payload(is_private=True)
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

    def test_update(self):
        payload = get_test_payload(is_private=True)
        headers = get_auth_headers(self.client, **self.CREDENTIALS)
        headers_admin = get_auth_headers(self.client, **self.CREDENTIALS_ADMIN)

        resp = self.client.post(reverse('tests-list'), data=payload, **headers)
        test = self.assertResp(resp)
        test_hash = test["hash"]

        other_payload = get_test_payload()
        del other_payload["questions"]

        resp = self.client.put(reverse('tests-detail', kwargs={'hash': test_hash}), data=other_payload, **headers_admin)
        self.assertWrongResp(resp, 403)

        resp = self.client.put(reverse('tests-detail', kwargs={'hash': test_hash}), data=other_payload, **headers)
        new_test = self.assertResp(resp)
        self.assertEqual(new_test["title"], other_payload["title"])

        resp = self.client.get(reverse('tests-detail', kwargs={'hash': test_hash}))
        new_test = self.assertResp(resp)
        self.assertEqual(new_test["title"], other_payload["title"])

    def test_delete(self):
        payload = get_test_payload(is_private=True)
        headers = get_auth_headers(self.client, **self.CREDENTIALS)
        headers_admin = get_auth_headers(self.client, **self.CREDENTIALS_ADMIN)

        resp = self.client.post(reverse('tests-list'), data=payload, **headers)
        test = self.assertResp(resp)
        test_hash = test["hash"]

        resp = self.client.delete(reverse('tests-detail', kwargs={'hash': test_hash}), **headers_admin)
        self.assertWrongResp(resp, 403)

        resp = self.client.delete(reverse('tests-detail', kwargs={'hash': test_hash}), **headers)
        self.assertResp(resp)

        resp = self.client.get(reverse('tests-detail', kwargs={'hash': test_hash}))
        self.assertWrongResp(resp, 404)


@override_settings(**TEST_SETTINGS)
class QuestionsModifyApi(APITestCaseEx):
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

    def setUp(self):
        payload = get_test_payload()
        headers = get_auth_headers(self.client, **self.CREDENTIALS)
        resp = self.client.post(reverse('tests-list'), data=payload, **headers)
        test = self.assertResp(resp)
        self.hash = test["hash"]

    def test_create(self):
        payload = get_test_payload()["questions"][0]
        headers = get_auth_headers(self.client, **self.CREDENTIALS)
        headers_admin = get_auth_headers(self.client, **self.CREDENTIALS_ADMIN)

        resp = self.client.get(reverse('tests-detail', kwargs={'hash': self.hash}))
        test_before = self.assertResp(resp)

        resp = self.client.post(reverse('questions-list', kwargs={'test_hash': self.hash}), data=payload,
                                **headers_admin)
        self.assertWrongResp(resp, 403)

        resp = self.client.post(reverse('questions-list', kwargs={'test_hash': self.hash}), data=payload, **headers)
        question = self.assertResp(resp)
        self.assertTrue(0 < len(question["answers"]) == len(payload["answers"]))

        resp = self.client.get(reverse('tests-detail', kwargs={'hash': self.hash}))
        test_after = self.assertResp(resp)

        self.assertTrue(len(test_after["questions"]) - len(test_before["questions"]) == 1)

    def test_update(self):
        payload = get_test_payload()["questions"][0]
        del payload["answers"]
        headers = get_auth_headers(self.client, **self.CREDENTIALS)
        headers_admin = get_auth_headers(self.client, **self.CREDENTIALS_ADMIN)

        resp = self.client.get(reverse('tests-detail', kwargs={'hash': self.hash}))
        test_before = self.assertResp(resp)
        question_id = choice(test_before["questions"])["id"]

        resp = self.client.put(reverse('questions-detail', kwargs={'test_hash': self.hash, 'pk': question_id}),
                               data=payload, **headers_admin)
        self.assertWrongResp(resp, 403)

        resp = self.client.put(reverse('questions-detail', kwargs={'test_hash': self.hash, 'pk': question_id}),
                               data=payload, **headers)
        self.assertResp(resp)

        resp = self.client.get(reverse('questions-detail', kwargs={'test_hash': self.hash, 'pk': question_id}))
        new_question = self.assertResp(resp)
        self.assertEqual(new_question["text"], payload["text"])

    def test_delete(self):
        headers = get_auth_headers(self.client, **self.CREDENTIALS)
        headers_admin = get_auth_headers(self.client, **self.CREDENTIALS_ADMIN)

        resp = self.client.get(reverse('tests-detail', kwargs={'hash': self.hash}))
        test_before = self.assertResp(resp)
        question_id = choice(test_before["questions"])["id"]

        resp = self.client.delete(reverse('questions-detail', kwargs={'test_hash': self.hash, 'pk': question_id}),
                                  **headers_admin)
        self.assertWrongResp(resp, 403)

        resp = self.client.delete(reverse('questions-detail', kwargs={'test_hash': self.hash, 'pk': question_id}),
                                  **headers)
        self.assertResp(resp)

        resp = self.client.get(reverse('questions-detail', kwargs={'test_hash': self.hash, 'pk': question_id}))
        self.assertWrongResp(resp, 404)


@override_settings(**TEST_SETTINGS)
class AnswersModifyApi(APITestCaseEx):
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

    def setUp(self):
        payload = get_test_payload()
        headers = get_auth_headers(self.client, **self.CREDENTIALS)
        resp = self.client.post(reverse('tests-list'), data=payload, **headers)
        test = self.assertResp(resp)
        self.hash = test["hash"]
        self.question_id = choice(test["questions"])["id"]
        self.params_n = len(test["params"])

    def get_payload(self, params_n):
        return {
            "position": 1000,
            "text": random_text.random_paragraph((20, 30), (1, 2)),
            "params_value": [randint(0, 3) for _ in range(params_n)]
        }

    def test_create(self):
        headers = get_auth_headers(self.client, **self.CREDENTIALS)
        headers_admin = get_auth_headers(self.client, **self.CREDENTIALS_ADMIN)

        resp = self.client.get(reverse('questions-detail', kwargs={'test_hash': self.hash, 'pk': self.question_id}))
        question_before = self.assertResp(resp)

        payload = self.get_payload(self.params_n)

        resp = self.client.post(
            reverse('answers-list', kwargs={'test_hash': self.hash, 'question_pk': self.question_id}),
            data=payload,
            **headers_admin
        )
        self.assertWrongResp(resp, 403)

        resp = self.client.post(
            reverse('answers-list', kwargs={'test_hash': self.hash, 'question_pk': self.question_id}),
            data=payload,
            **headers
        )
        self.assertResp(resp)

        resp = self.client.get(reverse('questions-detail', kwargs={'test_hash': self.hash, 'pk': self.question_id}))
        question_after = self.assertResp(resp)

        self.assertTrue(len(question_after["answers"]) - len(question_before["answers"]) == 1)

    def test_update(self):
        headers = get_auth_headers(self.client, **self.CREDENTIALS)
        headers_admin = get_auth_headers(self.client, **self.CREDENTIALS_ADMIN)

        resp = self.client.get(reverse('questions-detail', kwargs={'test_hash': self.hash, 'pk': self.question_id}))
        question_before = self.assertResp(resp)
        answer_id = choice(question_before["answers"])["id"]

        payload = self.get_payload(self.params_n)

        resp = self.client.put(
            reverse(
                'answers-detail',
                kwargs={'test_hash': self.hash, 'question_pk': self.question_id, 'pk': answer_id}
            ),
            data=payload,
            **headers_admin
        )
        self.assertWrongResp(resp, 403)

        resp = self.client.put(
            reverse(
                'answers-detail',
                kwargs={'test_hash': self.hash, 'question_pk': self.question_id, 'pk': answer_id}
            ),
            data=payload,
            **headers
        )
        self.assertResp(resp)

        resp = self.client.get(reverse(
            'answers-detail',
            kwargs={'test_hash': self.hash, 'question_pk': self.question_id, 'pk': answer_id}
        ))
        new_answer = self.assertResp(resp)
        self.assertEqual(new_answer["text"], payload["text"])

    def test_delete(self):
        headers = get_auth_headers(self.client, **self.CREDENTIALS)
        headers_admin = get_auth_headers(self.client, **self.CREDENTIALS_ADMIN)

        resp = self.client.get(reverse('questions-detail', kwargs={'test_hash': self.hash, 'pk': self.question_id}))
        question_before = self.assertResp(resp)
        answer_id = choice(question_before["answers"])["id"]

        resp = self.client.delete(reverse(
            'answers-detail',
            kwargs={'test_hash': self.hash, 'question_pk': self.question_id, 'pk': answer_id}
        ), **headers_admin)
        self.assertWrongResp(resp, 403)

        resp = self.client.delete(reverse(
            'answers-detail',
            kwargs={'test_hash': self.hash, 'question_pk': self.question_id, 'pk': answer_id}
        ), **headers)
        self.assertResp(resp)

        resp = self.client.get(reverse(
            'answers-detail',
            kwargs={'test_hash': self.hash, 'question_pk': self.question_id, 'pk': answer_id}
        ))
        self.assertWrongResp(resp, 404)


@override_settings(**TEST_SETTINGS)
class UsersAnswersApi(QuestionsTestData, APITestCaseEx):
    def test_give_single_answer(self):
        headers = get_auth_headers(self.client, **self.CREDENTIALS)
        test = models.Test.objects.first()
        question = test.questions.first()
        answer = question.answers.first()

        resp = self.client.post(reverse(
            'answers-give',
            kwargs={'test_hash': test.hash, 'question_pk': question.id, 'pk': answer.id}
        ), **headers)
        self.assertResp(resp)

    def test_give_multiple_answers(self):
        headers = get_auth_headers(self.client, **self.CREDENTIALS)
        test = models.Test.objects.first()

        for question in test.questions.iterator():
            answer = question.answers.first()
            resp = self.client.post(reverse(
                'answers-give',
                kwargs={'test_hash': test.hash, 'question_pk': question.id, 'pk': answer.id}
            ), **headers)
            self.assertResp(resp)

        self.assertEqual(
            test.questions.count(),
            models.UserAnswers.objects.get(user__username=self.CREDENTIALS["username"], test=test).choices.count()
        )

    def test_give_multiple_answers_and_change(self):
        headers = get_auth_headers(self.client, **self.CREDENTIALS)
        test = models.Test.objects.first()

        for question in test.questions.iterator():
            answer = question.answers.first()
            resp = self.client.post(reverse(
                'answers-give',
                kwargs={'test_hash': test.hash, 'question_pk': question.id, 'pk': answer.id}
            ), **headers)
            self.assertResp(resp)

        for question in list(test.questions.all())[::-1]:
            answer = question.answers.last()
            resp = self.client.post(reverse(
                'answers-give',
                kwargs={'test_hash': test.hash, 'question_pk': question.id, 'pk': answer.id}
            ), **headers)
            self.assertResp(resp)

        self.assertEqual(
            test.questions.count(),
            models.UserAnswers.objects.get(user__username=self.CREDENTIALS["username"], test=test).choices.count()
        )
