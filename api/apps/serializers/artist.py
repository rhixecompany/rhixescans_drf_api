from rest_framework import serializers
from django.db.models import Q
from api.apps.models import Artist


class ArtistSerializer(serializers.ModelSerializer[Artist]):
    class Meta:
        model = Artist
        fields = ("name",)

    def validate_name(self, value):
        artist = Artist.objects.filter(Q(name__iexact=value)).first()
        if artist:
            raise serializers.ValidationError("Artist with this Name already exists.")
        return value
