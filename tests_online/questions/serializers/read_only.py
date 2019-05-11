from typing import Optional

from rest_framework import serializers

from .. import models


class AnswerReadOnlySerializer(serializers.ModelSerializer):
    is_user_answer = serializers.SerializerMethodField()

    def get_is_user_answer(self, answer: models.Answer) -> Optional[bool]:
        user_answers: models.UserAnswers = self.context.get("user_answers", None)
        return user_answers and user_answers.choices.filter(pk=answer.pk).exists()

    class Meta:
        model = models.Answer
        fields = ('id', 'position', 'text', 'params_value', 'is_user_answer')


class QuestionReadOnlySerializer(serializers.ModelSerializer):
    answers = AnswerReadOnlySerializer(many=True, read_only=True)

    class Meta:
        model = models.Question
        fields = ('id', 'position', 'text', 'answers')


class TestReadOnlySerializer(serializers.ModelSerializer):
    stats_restriction_display = serializers.CharField(source='get_stats_restriction_display')
    questions = QuestionReadOnlySerializer(many=True, read_only=True)

    class Meta:
        model = models.Test
        fields = ('id', 'hash', 'title', 'description', 'is_private', 'params', 'params_defaults',
                  'stats_restriction', 'stats_restriction_display', 'owner', 'questions')


class TestReadOnlyShortSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='tests-detail', read_only=True, lookup_field='hash')
    owner = serializers.CharField(source="owner_name")
    questions_number = serializers.IntegerField()
    user_answers = serializers.SerializerMethodField()

    def get_user_answers(self, test: models.Test) -> Optional[int]:
        return getattr(test, 'user_answers', None)

    class Meta:
        model = models.Test
        fields = ('id', 'url', 'hash', 'title', 'description', 'params', 'stats_restriction', 'owner',
                  'questions_number', 'user_answers',)


class TestResultsSerializer(serializers.Serializer):
    is_complete = serializers.BooleanField()
    results = serializers.JSONField()
