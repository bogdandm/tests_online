from rest_framework import serializers

from .. import models


class AnswerReadOnlySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ('id', 'position', 'params_value')


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
    url = serializers.HyperlinkedIdentityField(view_name='tests-detail', lookup_field='hash', read_only=True)
    owner = serializers.StringRelatedField()

    class Meta:
        model = models.Test
        fields = ('id', 'url', 'hash', 'title', 'params', 'stats_restriction', 'owner')


