from api.apps.serializers.user import UserSerializer
from api.apps.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.shortcuts import get_object_or_404


@api_view(["GET"])
def user_list(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    serializer = UserSerializer(user)

    return Response(serializer.data)
