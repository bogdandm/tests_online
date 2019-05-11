from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.viewsets import GenericViewSet

from core.permissions import ActionCombiner
from . import serializers


class UserViewSet(GenericViewSet):
    pagination_class = None
    permission_classes = [ActionCombiner({
        "info": IsAuthenticated,
        "signup": True
    })]

    def get_serializer_class(self):
        return {
            "info": serializers.UserSerializer,
            "signup": serializers.SignUpSerializer
        }.get(self.action, Serializer)

    def get_object(self):
        return self.request.user

    @action(detail=False, methods=['get'])
    def info(self, request):
        user = self.get_object()
        return Response(self.get_serializer(instance=user).data)

    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(self.get_serializer(instance=user).data)
