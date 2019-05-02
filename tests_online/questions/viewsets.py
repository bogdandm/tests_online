from rest_framework import permissions, viewsets
from rest_framework.serializers import Serializer

from core.permissions import ActionCombiner, AndCombiner as And, ObjectOwner
from . import models, serializers


class TestsViewSet(viewsets.ModelViewSet):
    queryset = models.Test.objects.all()
    lookup_url_kwarg = 'hash'
    lookup_field = 'hash'
    permission_classes = [ActionCombiner({
        'list': True,
        'retrieve': True,

        'create': permissions.IsAuthenticated,
        'update': And(permissions.IsAuthenticated, ObjectOwner),
        'partial_update': And(permissions.IsAuthenticated, ObjectOwner),
        'delete': And(permissions.IsAuthenticated, ObjectOwner),
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
               }.get(self.action, None) or Serializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
