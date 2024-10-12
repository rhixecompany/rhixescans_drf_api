from rest_framework import serializers
from django.db.models import Q
from api.apps.models import Genre


class GenreSerializer(serializers.ModelSerializer[Genre]):
    class Meta:
        model = Genre
        fields = ("name",)

    def validate_name(self, value):
        genre = Genre.objects.filter(Q(name__iexact=value)).first()
        if genre:
            raise serializers.ValidationError("Genre with this Name already exists.")
        return value
