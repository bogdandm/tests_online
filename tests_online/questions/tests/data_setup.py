from random import randint, random

from django.contrib.auth import get_user_model
from django.test import TestCase

from core.tests import random_text
from .. import models


class QuestionsTestData(TestCase):
    CREDENTIALS = {
        "username": "test_admin",
        "email": "",
        "password": "qwerty12"
    }

    @classmethod
    def setUpTestData(cls):
        cls.User = get_user_model()
        cls.user = cls.User.objects.filter(username=cls.CREDENTIALS["username"]).first()
        if cls.user is None:
            cls.user = cls.User.objects.create_superuser(**cls.CREDENTIALS)

        cls.public_test: models.Test
        cls.private_test: models.Test
        for is_private, attrname in ((False, "public_test"), (True, "private_test")):
            test = models.Test.objects.create(
                title=attrname,
                description=random_text.random_paragraph((20, 30), (3, 7)),
                is_private=is_private,
                params=[f"Param{n}" for n in range(1, 10)],
                params_defaults=[float(randint(0, 9)) for _ in range(1, 10)],
                stats_restriction=models.TestStatsChoices.ANY,
                owner=cls.user
            )
            setattr(cls, attrname, test)

        test: models.Test
        for test in models.Test.objects.iterator():
            for i in range(randint(4, 10)):
                question = models.Question.objects.create(
                    position=i + 1,
                    text=random_text.random_paragraph((20, 30), (4, 6)),
                    test=test
                )

                for j in range(randint(2, 5)):
                    answer = models.Answer.objects.create(
                        position=i + 1,
                        text=random_text.random_paragraph((20, 30), (4, 6)),
                        params_value=[x + random() * 2 - 1 for x in test.params_defaults],
                        question=question
                    )
