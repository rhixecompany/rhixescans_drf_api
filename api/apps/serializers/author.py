from rest_framework import serializers
from django.db.models import Q
from api.apps.models import Author


class AuthorSerializer(serializers.ModelSerializer[Author]):
    class Meta:
        model = Author
        fields = ("name",)

    def validate_name(self, value):
        author = Author.objects.filter(Q(name__iexact=value)).first()
        if author:
            raise serializers.ValidationError("Author with this Name already exists.")
        return value
