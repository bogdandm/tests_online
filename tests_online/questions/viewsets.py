from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from core.permissions import ActionCombiner, AndCombiner as And, BasePermissionEx, ObjectOwner
from core.views import CachedObjectMixin
from . import models, serializers


class TestsViewSet(viewsets.ModelViewSet, CachedObjectMixin):
    queryset = models.Test.objects.all()
    lookup_url_kwarg = 'hash'
    lookup_field = 'hash'
    permission_classes = [ActionCombiner({
        'list': True,
        'retrieve': True,

        'create': permissions.IsAuthenticated,
        'update': And(permissions.IsAuthenticated, ObjectOwner()),
        'partial_update': And(permissions.IsAuthenticated, ObjectOwner()),
        'destroy': And(permissions.IsAuthenticated, ObjectOwner()),
    })]

    def filter_queryset(self, queryset):
        if self.action == "list":
            qs = queryset.filter(is_private=False)
            if self.request.auth:
                user = self.request.auth.user
            elif self.request.user:
                user = self.request.user
            else:
                return qs

            if not user.is_anonymous:
                return qs | queryset.filter(is_private=True, owner=user)
            return qs
        else:
            return queryset

    def get_serializer_class(self):
        return {
            "list": serializers.TestReadOnlyShortSerializer,
            "create": serializers.TestSerializer,
            "retrieve": serializers.TestReadOnlySerializer,
            "update": serializers.TestSerializer,
            "partial_update": serializers.TestSerializer
        }.get(self.action, Serializer)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if self.action == "retrieve" and self.request.user and not self.request.user.is_anonymous:
            test = self.get_object()
            user = self.request.user
            user_answers = models.UserAnswers.objects.filter(test=test, user=user).first()
        else:
            user_answers = None
        context["user_answers"] = user_answers
        return context

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CreateTestPartPermission(BasePermissionEx):
    def has_permission_ex(self, request, view, obj):
        test_hash = view.kwargs["test_hash"]
        owner_id = models.Test.objects.filter(hash=test_hash).values_list('owner_id', flat=True)[0]
        return owner_id == request.user.id


class QuestionsViewSet(viewsets.ModelViewSet):
    queryset = models.Question.objects.all()

    modify_permission = And(permissions.IsAuthenticated, ObjectOwner('test.owner'))
    permission_classes = [ActionCombiner({
        'list': True,
        'retrieve': True,

        'create': And(permissions.IsAuthenticated, CreateTestPartPermission()),
        'update': modify_permission,
        'partial_update': modify_permission,
        'destroy': modify_permission,
    })]

    def filter_queryset(self, queryset):
        return queryset.filter(test__hash=self.kwargs["test_hash"])

    def get_serializer_class(self):
        return {
            "list": serializers.QuestionReadOnlySerializer,
            "create": serializers.QuestionSerializer,
            "retrieve": serializers.QuestionReadOnlySerializer,
            "update": serializers.QuestionSerializer,
            "partial_update": serializers.QuestionSerializer
        }.get(self.action, Serializer)

    def get_test_id(self):
        return models.Test.objects.filter(hash=self.kwargs["test_hash"]).values_list("id", flat=True)[0]

    def perform_create(self, serializer):
        serializer.save(test_id=self.get_test_id())

    def perform_update(self, serializer):
        serializer.save(test_id=self.get_test_id())


class AnswersViewSet(viewsets.ModelViewSet):
    queryset = models.Answer.objects.all()

    modify_permission = And(permissions.IsAuthenticated, ObjectOwner('question.test.owner'))
    permission_classes = [ActionCombiner({
        'list': True,
        'retrieve': True,

        'create': And(permissions.IsAuthenticated, CreateTestPartPermission()),
        'update': modify_permission,
        'partial_update': modify_permission,
        'destroy': modify_permission,

        'give': permissions.IsAuthenticated
    })]

    def filter_queryset(self, queryset):
        return queryset.filter(question_id=self.kwargs["question_pk"], question__test__hash=self.kwargs["test_hash"])

    def get_serializer_class(self):
        return {
            "list": serializers.AnswerReadOnlySerializer,
            "create": serializers.AnswerSerializer,
            "retrieve": serializers.AnswerReadOnlySerializer,
            "update": serializers.AnswerSerializer,
            "partial_update": serializers.AnswerSerializer
        }.get(self.action, Serializer)

    def perform_create(self, serializer):
        serializer.save(question_id=self.kwargs["question_pk"])

    def perform_update(self, serializer):
        serializer.save(question_id=self.kwargs["question_pk"])

    @action(detail=True, methods=['post'])
    def give(self, request, **pks):
        """
        Give answer with given pk as answer for question
        """
        answer = self.get_object()
        user = request.user
        question_id = answer.question_id
        test_id = models.Test.objects.filter(questions__id=question_id).values_list("id", flat=True)[0]

        answers_set: models.UserAnswers = models.UserAnswers.objects.filter(user=user, test_id=test_id).first()
        updated = False
        if answers_set is None:
            answers_set = models.UserAnswers.objects.create(user=user, test_id=test_id)
        else:
            old_answer = answers_set.choices.filter(question_id=question_id).first()
            if old_answer is not None:
                updated = True
                answers_set.choices.remove(old_answer)
        answers_set.choices.add(answer)

        return Response({"status": "added" if not updated else "updated"}, status=status.HTTP_201_CREATED)
