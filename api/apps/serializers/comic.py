from rest_framework import serializers

from api.apps.serializers.user import UsersItemSerializer
from api.apps.serializers.comicimage import (
    ComicImageItemSerializer,
)
from api.apps.serializers.genre import GenreSerializer
from api.apps.serializers.type import TypeSerializer
from api.apps.serializers.author import AuthorSerializer
from api.apps.serializers.artist import ArtistSerializer
from api.apps.serializers.chapter import ChapterSerializer

from api.apps.models import Comic
from django.db.models import Q


class ComicSerializer(serializers.ModelSerializer[Comic]):
    users = serializers.SerializerMethodField(read_only=True)
    chapters = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)

    genres = GenreSerializer(many=True, read_only=True)
    type = TypeSerializer(many=False, read_only=True)
    author = AuthorSerializer(many=False, read_only=True)
    artist = ArtistSerializer(many=False, read_only=True)

    class Meta:
        model = Comic
        fields = (
            "id",
            "title",
            "slug",
            "description",
            "status",
            "rating",
            "serialization",
            "numChapters",
            "spider",
            "url",
            "type",
            "genres",
            "author",
            "artist",
            "users",
            "images",
            "chapters",
        )

    def get_users(self, obj):
        users = obj.usersitem_set.all()
        serializer = UsersItemSerializer(users, many=True)
        return serializer.data

    def get_chapters(self, obj):
        chapters = obj.chapter_comic.all()
        serializer = ChapterSerializer(chapters, many=True)
        return serializer.data

    def get_images(self, obj):
        images = obj.comicimagesitem_set.all()
        serializer = ComicImageItemSerializer(images, many=True)
        return serializer.data

    def validate_numChapters(self, value):
        if value <= 0:
            raise serializers.ValidationError("Num_Chapters must be greater than 0.")
        return value

    def validate_title(self, value):
        comic = Comic.objects.filter(Q(title__iexact=value)).first()
        if comic:
            raise serializers.ValidationError("Comic with this Title already exists.")
        return value

    def validate_slug(self, value):
        comic = Comic.objects.filter(Q(slug__iexact=value)).first()
        if comic:
            raise serializers.ValidationError("Comic with this Slug already exists.")
        return value


class ComicsSerializer(serializers.HyperlinkedModelSerializer[Comic]):
    users = serializers.SerializerMethodField(read_only=True)
    chapters = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    type = TypeSerializer(many=False, read_only=True)
    author = AuthorSerializer(many=False, read_only=True)
    artist = ArtistSerializer(many=False, read_only=True)
    highlight = serializers.HyperlinkedIdentityField(
        view_name="comic", lookup_field="pk", format="html"
    )

    class Meta:
        model = Comic
        fields = (
            "id",
            "title",
            "slug",
            "description",
            "status",
            "rating",
            "serialization",
            "numChapters",
            "spider",
            # "url",
            "type",
            "genres",
            "author",
            "artist",
            "users",
            "images",
            "chapters",
            "highlight",
            "url",
        )

    def get_users(self, obj):
        users = obj.usersitem_set.all()
        serializer = UsersItemSerializer(users, many=True)
        return serializer.data

    def get_chapters(self, obj):
        chapters = obj.chapter_comic.all()
        serializer = ChapterSerializer(chapters, many=True)
        return serializer.data

    def get_images(self, obj):
        images = obj.comicimagesitem_set.all().first()
        serializer = ComicImageItemSerializer(images, many=False)
        return serializer.data

    def validate_numChapters(self, value):
        if value <= 0:
            raise serializers.ValidationError("Num_Chapters must be greater than 0.")
        return value

    def validate_title(self, value):
        comic = Comic.objects.filter(Q(title__iexact=value)).first()
        if comic:
            raise serializers.ValidationError("Comic with this Title already exists.")
        return value

    def validate_slug(self, value):
        comic = Comic.objects.filter(Q(slug__iexact=value)).first()
        if comic:
            raise serializers.ValidationError("Comic with this Slug already exists.")
        return value
