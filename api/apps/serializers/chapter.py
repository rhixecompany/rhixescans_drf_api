from rest_framework import serializers

# from api.apps.serializers.comic import ComicSerializer
from api.apps.serializers.chapterimage import ChapterImageSerializer
from api.apps.models import Chapter
from django.db.models import Q


class ChapterSerializer(serializers.ModelSerializer[Chapter]):
    # images = ChapterImageSerializer(many=True, read_only=True)
    # comic = ComicSerializer(many=False, read_only=True)
    updated_at = serializers.DateTimeField(format="iso-8601")
    comic_slug = serializers.URLField(source="comic.slug", read_only=True)
    comic_title = serializers.URLField(source="comic.title", read_only=True)

    class Meta:
        model = Chapter
        fields = (
            "id",
            "name",
            "slug",
            "spider",
            "url",
            "numPages",
            "updated_at",
            "comic_slug",
            "comic_title",
            # "images",
        )

    def validate_numPages(self, value):
        if value <= 0:
            raise serializers.ValidationError("Num_Pages must be greater than 0.")
        return value

    def validate_slug(self, value):
        chapter = Chapter.objects.filter(Q(slug__iexact=value)).first()
        if chapter:
            raise serializers.ValidationError("Chapter with this Slug already exists.")
        return value


class ChaptersSerializer(serializers.ModelSerializer[Chapter]):
    images = ChapterImageSerializer(many=True, read_only=True)
    # comic = ComicSerializer(many=False, read_only=True)
    comic_slug = serializers.URLField(source="comic.slug", read_only=True)
    comic_title = serializers.URLField(source="comic.title", read_only=True)

    class Meta:
        model = Chapter
        fields = (
            "id",
            "name",
            "slug",
            "spider",
            "url",
            "numPages",
            "comic_slug",
            "comic_title",
            "images",
        )

    def validate_numPages(self, value):
        if value <= 0:
            raise serializers.ValidationError("Num_Pages must be greater than 0.")
        return value

    def validate_slug(self, value):
        chapter = Chapter.objects.filter(Q(slug__iexact=value)).first()
        if chapter:
            raise serializers.ValidationError("Chapter with this Slug already exists.")
        return value
