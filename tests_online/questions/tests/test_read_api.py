import operator

from django.test import override_settings
from django.urls import reverse

from auth.test_utils import get_auth_headers
from core.tests.utils import APITestCaseEx, TEST_SETTINGS
from .data_setup import QuestionsTestData
from .. import models


@override_settings(**TEST_SETTINGS)
class TestReadApi(QuestionsTestData, APITestCaseEx):
    def test_list(self):
        resp = self.client.get(reverse('tests-list'))
        tests = self.assertResp(resp)["results"]
        self.assertEqual(len(tests), 1)
        self.assertEqual(tests[0]["title"], "public_test")

        headers = get_auth_headers(self.client, **self.CREDENTIALS)

        resp = self.client.get(reverse('tests-list'), **headers)
        tests = self.assertResp(resp)["results"]
        self.assertGreater(len(tests), 1)
        self.assertTrue("private_test" in map(operator.itemgetter('title'), tests))

    def test_retrieve(self):
        for h in models.Test.objects.values_list("hash", flat=True):
            resp = self.client.get(reverse('tests-detail', kwargs={'hash': h}))
            test = self.assertResp(resp)
            self.assertTrue(test["questions"])
            self.assertTrue(all(q["answers"] for q in test["questions"]))


@override_settings(**TEST_SETTINGS)
class QuestionTestApi(QuestionsTestData, APITestCaseEx):
    def test_list(self):
        test_hash = self.private_test.hash
        resp = self.client.get(reverse('questions-list', kwargs={'test_hash': test_hash}))
        questions = self.assertResp(resp)["results"]
        self.assertTrue(questions)

    def test_detail(self):
        test_hash = self.private_test.hash
        q_id = models.Question.objects.filter(test__hash=test_hash).first().id
        resp = self.client.get(reverse('questions-detail', kwargs={'test_hash': test_hash, 'pk': q_id}))
        question = self.assertResp(resp)
        self.assertTrue(question)


@override_settings(**TEST_SETTINGS)
class AnswersTestApi(QuestionsTestData, APITestCaseEx):
    def test_list(self):
        test_hash = self.private_test.hash
        q_id = models.Question.objects.filter(test__hash=test_hash).first().id
        resp = self.client.get(reverse('answers-list', kwargs={'test_hash': test_hash, 'question_pk': q_id}))
        answers = self.assertResp(resp)["results"]
        self.assertTrue(answers)

    def test_detail(self):
        test_hash = self.private_test.hash
        q_id = models.Question.objects.filter(test__hash=test_hash).first().id
        a_id = models.Answer.objects.filter(question_id=q_id).first().id
        resp = self.client.get(reverse('answers-detail',
                                       kwargs={'test_hash': test_hash, 'question_pk': q_id, 'pk': a_id}))
        answer = self.assertResp(resp)
        self.assertTrue(answer)
