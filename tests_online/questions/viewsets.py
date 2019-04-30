from rest_framework import viewsets
from rest_framework.serializers import Serializer

from . import models, serializers


class TestsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Test.objects.all()
    lookup_url_kwarg = 'hash'
    lookup_field = 'hash'

    def filter_queryset(self, queryset):
        qs = queryset.filter(is_private=False)
        if self.request.auth:
            user = self.request.auth.user
            if not user.is_anonymous:
                qs += queryset.filter(is_private=True, owner=user)
        return qs

    def get_serializer_class(self):
        return {
                   "list": serializers.TestReadOnlyShortSerializer,
                   "retrieve": serializers.TestReadOnlySerializer
               }.get(self.action, None) or Serializer
