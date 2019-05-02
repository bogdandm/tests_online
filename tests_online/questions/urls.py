from django.urls import include, path
from rest_framework_nested.routers import NestedSimpleRouter, SimpleRouter

from . import viewsets

tests_router = SimpleRouter()
tests_router.register('tests', viewsets.TestsViewSet, base_name='tests')

questions_router = NestedSimpleRouter(tests_router, 'tests', lookup='test')
questions_router.register('questions', viewsets.QuestionsViewSet, base_name='questions')

answers_router = NestedSimpleRouter(questions_router, 'questions', lookup='question')
answers_router.register('answers', viewsets.AnswersViewSet, base_name='answers')

urlpatterns = [
    path('', include(tests_router.get_urls())),
    path('', include(questions_router.get_urls())),
    path('', include(answers_router.get_urls())),
]
