from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from .. import models


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ('id', 'position', 'params_value')
        read_only_fields = ('id',)


class QuestionSerializer(WritableNestedModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = models.Question
        fields = ('id', 'position', 'text', 'answers')
        read_only_fields = ('id',)


class TestSerializer(WritableNestedModelSerializer):
    stats_restriction_display = serializers.CharField(source='get_stats_restriction_display', read_only=True)
    questions = QuestionSerializer(many=True)
    owner = serializers.StringRelatedField()

    def validate(self, attrs):
        attrs = super().validate(attrs)
        n = len(attrs["params"]) if "params" in attrs else 1
        if (len(attrs["params_default"]) if "params" in attrs else 1) != n:
            raise models.Test.TestParamsError("params", "params_default")
        for q in attrs["questions"]:
            for a in q["answers"]:
                if len(a["params_value"]) != n:
                    raise models.Test.TestParamsError('params_value', 'test.params')
        return attrs

    class Meta:
        model = models.Test
        fields = ('id', 'hash', 'title', 'description', 'is_private', 'params', 'params_defaults',
                  'stats_restriction', 'stats_restriction_display', 'owner', 'questions')
        read_only_fields = ('id', 'hash', 'stats_restriction_display', 'owner')
