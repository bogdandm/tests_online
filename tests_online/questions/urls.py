from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import viewsets

tests_router = DefaultRouter()
tests_router.register('', viewsets.TestsViewSet, base_name='tests')

urlpatterns = [
    path('tests/', include(tests_router.get_urls())),
]
