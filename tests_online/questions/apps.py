from django.apps import AppConfig, apps
from django.db.models.signals import post_delete, post_save


def post_save_test(sender, test, created, *args, **kwargs):
    if not created:
        test.clear_params_bounds()


def post_save_answer(sender, answer, created, *args, **kwargs):
    Test = apps.get_model(QuestionsConfig.name, "Test")
    test = Test.objects.filter(questions__id=answer.question_id).only("id", "params")
    test.clear_params_bounds()


def post_delete_question(sender, question, *args, **kwargs):
    Test = apps.get_model(QuestionsConfig.name, "Test")
    test = Test.objects.filter(questions__id=question.id).only("id", "params")
    test.clear_params_bounds()


def post_delete_answer(sender, answer, *args, **kwargs):
    Test = apps.get_model(QuestionsConfig.name, "Test")
    test = Test.objects.filter(questions__id=answer.question_id).only("id", "params")
    test.clear_params_bounds()


class QuestionsConfig(AppConfig):
    name = 'questions'

    def ready(self):
        post_save.connect(post_save_test, sender=self.get_model("Test"))
        post_save.connect(post_save_answer, sender=self.get_model("Answer"))
        post_delete.connect(post_delete_question, sender=self.get_model("Question"))
        post_delete.connect(post_delete_answer, sender=self.get_model("Answer"))
