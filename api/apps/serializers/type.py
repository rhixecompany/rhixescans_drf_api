from rest_framework import serializers
from django.db.models import Q

from api.apps.models import Type


class TypeSerializer(serializers.ModelSerializer[Type]):
    class Meta:
        model = Type
        fields = ("name",)

    def validate_name(self, value):
        type = Type.objects.filter(Q(name__iexact=value)).first()
        if type:
            raise serializers.ValidationError("Type with this Name already exists.")
        return value
