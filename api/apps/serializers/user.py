from rest_framework import serializers

from api.users.models import User
from api.apps.models import UsersItem


class UserSerializer(serializers.ModelSerializer[User]):

    class Meta:
        model = User
        fields = (  # "url",
            "username",
            "email",
            "first_name",
            "last_name",
            "images",
            "is_staff",
        )

        # extra_kwargs = {
        #     "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        # }


class UsersItemSerializer(serializers.ModelSerializer[UsersItem]):

    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = UsersItem
        fields = (
            "user",
            "comic",
            "order",
        )
