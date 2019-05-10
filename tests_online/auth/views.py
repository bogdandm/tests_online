from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from . import serializers


@api_view()
@permission_classes((IsAuthenticated,))
def get_current_user(request):
    user = request.user
    return Response(serializers.UserSerializer(user).data)
