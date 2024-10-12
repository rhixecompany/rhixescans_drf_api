from rest_framework import serializers
from django.db.models import Q
from api.apps.models import ComicImage, ComicImagesItem


class ComicImageItemSerializer(serializers.ModelSerializer[ComicImagesItem]):
    link_url = serializers.URLField(source="link.url", read_only=True)
    comic_slug = serializers.URLField(source="comic.slug", read_only=True)

    class Meta:
        model = ComicImagesItem
        fields = (
            "image",
            "link_url",
            "comic_slug",
        )


class ComicImageSerializer(serializers.ModelSerializer[ComicImage]):
    url = serializers.URLField()
    images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ComicImage
        fields = (
            "url",
            "images",
        )

    def validate_url(self, value):
        comicImage = ComicImage.objects.filter(Q(url__iexact=value)).first()
        if comicImage:
            raise serializers.ValidationError(
                "ComicImage with this url already exists."
            )
        return value

    def get_images(self, obj):
        images = obj.comic_photo.all()
        serializer = ComicImageItemSerializer(images, many=True)
        return serializer.data


class ComicImagesSerializer(serializers.ModelSerializer[ComicImage]):
    url = serializers.URLField()
    images = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ComicImage
        fields = (
            "url",
            "images",
        )

    def validate_url(self, value):
        comicImage = ComicImage.objects.filter(Q(url__iexact=value)).first()
        if comicImage:
            raise serializers.ValidationError(
                "ComicImage with this url already exists."
            )
        return value

    def get_images(self, obj):
        images = obj.comic_photo.all()[0:1]
        serializer = ComicImageItemSerializer(images, many=True)
        return serializer.data
