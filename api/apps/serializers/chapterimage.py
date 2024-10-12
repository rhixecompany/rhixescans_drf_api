from rest_framework import serializers
from django.db.models import Q
from api.apps.models import ChapterImage, ChapterImagesItem


class ChapterImageItemSerializer(serializers.ModelSerializer[ChapterImagesItem]):
    link_url = serializers.URLField(source="link.url", read_only=True)
    chapter_slug = serializers.URLField(source="chapter.slug", read_only=True)
    comic_slug = serializers.URLField(source="comic.slug", read_only=True)

    class Meta:
        model = ChapterImagesItem
        fields = (
            "image",
            "link_url",
            "chapter_slug",
            "comic_slug",
        )


class ChapterImageSerializer(serializers.ModelSerializer[ChapterImage]):
    url = serializers.URLField()
    images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ChapterImage
        fields = (
            "url",
            "images",
        )

    def validate_url(self, value):
        chapterImage = ChapterImage.objects.filter(Q(url__iexact=value)).first()
        if chapterImage:
            raise serializers.ValidationError(
                "ChapterImage with this url already exists."
            )
        return value

    def get_images(self, obj):
        images = obj.chapter_photo.all()
        serializer = ChapterImageItemSerializer(images, many=True)
        return serializer.data
