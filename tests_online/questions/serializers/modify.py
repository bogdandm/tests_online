from drf_writable_nested import NestedCreateMixin
from rest_framework import serializers

from .. import models


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ('id', 'position', 'params_value')
        read_only_fields = ('id',)


class QuestionSerializer(NestedCreateMixin, serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    def update(self, instance, validated_data):
        validated_data.pop("answers")
        return super().update(instance, validated_data)

    class Meta:
        model = models.Question
        fields = ('id', 'position', 'text', 'answers')
        read_only_fields = ('id',)


class TestSerializer(NestedCreateMixin, serializers.ModelSerializer):
    stats_restriction_display = serializers.CharField(source='get_stats_restriction_display', read_only=True)
    questions = QuestionSerializer(many=True)
    owner = serializers.StringRelatedField()

    class Meta:
        model = models.Test
        fields = ('id', 'hash', 'title', 'description', 'is_private', 'params', 'params_defaults',
                  'stats_restriction', 'stats_restriction_display', 'owner', 'questions')
        read_only_fields = ('id', 'hash', 'stats_restriction_display', 'owner')

    def validate(self, attrs: dict):
        attrs = super().validate(attrs)
        n = len(attrs["params"]) if "params" in attrs else 1

        if (len(attrs["params_defaults"]) if "params_defaults" in attrs else 1) != n:
            raise models.Test.TestParamsError("params", "params_defaults")

        if "questions" in attrs:
            for question in attrs["questions"]:
                if "answers" in question:
                    for answer in question["answers"]:
                        if len(answer["params_value"]) != n:
                            raise models.Test.TestParamsError('params_value', 'test.params')
        return attrs

    def update(self, instance, validated_data):
        validated_data.pop("questions")
        return super().update(instance, validated_data)
