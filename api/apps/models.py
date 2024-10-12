# models.py
import uuid

# from django.forms import ValidationError
# import magic
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

from api.apps.managers import NewManager

User = get_user_model()


def panel_location(instance, filename):
    return "{}/{}/{}".format(
        str(instance.comic.slug)
        .replace(" ", "_")
        .replace(":", " ")
        .replace("/", "")
        .replace("\\", ""),
        instance.chapter.slug,
        filename,
    )


def comic_location(instance, filename):
    return "{}/{}".format(
        str(instance.comic.slug)
        .replace(" ", "_")
        .replace(":", " ")
        .replace("/", "")
        .replace("\\", ""),
        filename,
    )


ext_validator = FileExtensionValidator(
    [
        "ico",
        "jpg",
        "svg",
        "jpeg",
        "png",
        "gif",
        "bmp",
        "webp",
        "tiff",
        "ttf",
        "eot",
        "woff",
        "woff2",
    ],
)


# def validate_file_mimetype(file):
#     accept = [
#         "image/ico",
#         "image/jpg",
#         "image/svg",
#         "image/jpeg",
#         "image/png",
#         "image/gif",
#         "image/bmp",
#         "image/webp",
#         "image/tiff",
#         "image/tff",
#         "image/eot",
#         "image/woff",
#         "image/woff2",
#     ]
#     file_mime_type = magic.from_buffer(file.read(1024), mime=True)
#     print(file_mime_type)
#     if file_mime_type not in accept:
#         raise ValidationError("Unsupported file type")


class Genre(models.Model):
    name = models.CharField(_("Name"), max_length=200, unique=True)

    class Meta:
        verbose_name_plural = "Genres"

    def __str__(self):
        return f"{self.name}"

    # def get_absolute_url(self) -> str:
    #     return reverse("genre:detail", kwargs={"pk": self.pk})


class Author(models.Model):
    name = models.CharField(_("Name"), max_length=200, unique=True)

    class Meta:
        verbose_name_plural = "Authors"

    def __str__(self):
        return f"{self.name}"

    # def get_absolute_url(self) -> str:
    #     return reverse("author:detail", kwargs={"pk": self.pk})


class Artist(models.Model):
    name = models.CharField(_("Name"), max_length=200, unique=True)

    class Meta:
        verbose_name_plural = "Artists"

    def __str__(self):
        return f"{self.name}"

    # def get_absolute_url(self) -> str:
    #     return reverse("artist:detail", kwargs={"pk": self.pk})


class Type(models.Model):
    class TypeStatus(models.TextChoices):

        MANGA = "Manga"
        MANHWA = "Manhwa"
        MANHUA = "Manhua"

    name = models.CharField(
        _("Name"),
        max_length=6,
        choices=TypeStatus.choices,
    )

    class Meta:
        verbose_name_plural = "Types"

    def __str__(self):
        return f"{self.name}"

    # def get_absolute_url(self) -> str:
    #     return reverse("type:detail", kwargs={"pk": self.pk})


class ComicImage(models.Model):
    url = models.URLField(_("Url"), unique=True, max_length=500)

    def __str__(self):
        return f"{self.url}"


class Comic(models.Model):
    class ComicStatus(models.TextChoices):

        COMPLETED = "Completed"
        ONGOING = "Ongoing"
        HIATUS = "Hiatus"
        DROPPED = "Dropped"
        SEASON_END = "Season End"
        COMING_SOON = "Coming Soon"

    uuid = models.UUIDField(_("Uuid"), default=uuid.uuid4, editable=False)
    title = models.CharField(_("Title"), max_length=500, unique=True)
    slug = models.SlugField(_("Slug"), max_length=500, unique=True)
    description = models.TextField(_("Description"))
    status = models.CharField(
        _("Status"),
        max_length=15,
        choices=ComicStatus.choices,
    )
    rating = models.DecimalField(_("Rating"), max_digits=10, decimal_places=1)
    serialization = models.CharField(
        _("Serialization"),
        max_length=500,
        null=True,
        blank=True,
    )
    numChapters = models.PositiveIntegerField(_("Total Chapters"))
    spider = models.CharField(_("Spider"), max_length=500)
    url = models.URLField(_("Url"), max_length=500)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name="comic_type")
    genres = models.ManyToManyField(Genre, blank=True)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, blank=True, related_name="comic_author"
    )
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, blank=True, related_name="comic_artist"
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    users = models.ManyToManyField(
        User, related_name="comics", through="UsersItem", blank=True
    )
    images = models.ManyToManyField(
        ComicImage, related_name="pictures", through="ComicImagesItem"
    )

    objects = NewManager.as_manager()

    class Meta:
        verbose_name_plural = "Comics"
        ordering = ["-updated_at"]

    @property
    def has_chapters(self):
        return self.numChapters > 0

    def __str__(self):
        return f"{self.title}"

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("comic", kwargs={"pk": self.pk})

    def update_absolute_url(self) -> str:
        """POST URL for user's update view.

        Returns:
            str: URL for user update.

        """
        return reverse("comics:update-comic", kwargs={"pk": self.pk})

    def delete_absolute_url(self) -> str:
        """Delete URL for user's delete view.

        Returns:
            str: URL for user delete.

        """
        return reverse("comics:delete-comic", kwargs={"pk": self.pk})


class ComicImagesItem(models.Model):

    link = models.ForeignKey(
        ComicImage, on_delete=models.CASCADE, related_name="comic_photo"
    )
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE)
    image = models.ImageField(
        _("Image"),
        upload_to=comic_location,
        validators=[
            ext_validator,
            # validate_file_mimetype
        ],
        max_length=500,
    )

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.image}"

    def save(self, *args, **kwargs):
        if self.pk:
            existing = get_object_or_404(ComicImagesItem, pk=self.pk)
            if existing.image != self.image:
                existing.image.delete(save=False)

        super().save(*args, **kwargs)


class UsersItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField(
        _("Order"),
    )

    class Meta:
        ordering = ["order"]
        verbose_name_plural = "UsersItem"

    def __str__(self):
        return (
            f"Order - {self.order} User - {self.user.email} Comic - {self.comic.title}"
        )


class ChapterImage(models.Model):
    url = models.URLField(_("Url"), unique=True, max_length=500)

    def __str__(self):
        return f"{self.url}"


class Chapter(models.Model):
    uuid = models.UUIDField(_("Uuid"), default=uuid.uuid4, editable=False)
    name = models.CharField(_("Name"), max_length=500)
    slug = models.SlugField(_("Slug"), max_length=500, unique=True)
    spider = models.CharField(_("Spider"), max_length=500)
    url = models.URLField(_("Url"), max_length=500)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(
        null=True,
        blank=True,
    )
    numPages = models.PositiveSmallIntegerField(_("Total Pages"))
    comic = models.ForeignKey(
        Comic,
        on_delete=models.CASCADE,
        related_name="chapter_comic",
    )
    images = models.ManyToManyField(
        ChapterImage, related_name="pages", through="ChapterImagesItem"
    )

    class Meta:
        verbose_name_plural = "Chapters"
        ordering = ["-updated_at"]

    @property
    def has_pages(self):
        return self.numPages > 0

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("chapters:detail", kwargs={"pk": self.pk})

    def update_absolute_url(self) -> str:
        """POST URL for user's update view.

        Returns:
            str: URL for user update.

        """
        return reverse("chapters:update-chapter", kwargs={"pk": self.pk})

    def delete_absolute_url(self) -> str:
        """Delete URL for user's delete view.

        Returns:
            str: URL for user delete.

        """
        return reverse("chapters:delete-chapter", kwargs={"pk": self.pk})


class ChapterImagesItem(models.Model):
    link = models.ForeignKey(
        ChapterImage, on_delete=models.CASCADE, related_name="chapter_photo"
    )
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE)
    image = models.ImageField(
        _("Image"), upload_to=panel_location, validators=[ext_validator], max_length=500
    )

    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.image}"

    def save(self, *args, **kwargs):
        if self.pk:
            existing = get_object_or_404(ChapterImagesItem, pk=self.pk)
            if existing.image != self.image:
                existing.image.delete(save=False)

        super().save(*args, **kwargs)


class Comment(models.Model):
    body = CKEditor5Field(_("Body"), null=True, blank=True)
    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        related_name="comment_chapter",
    )
    user = models.ForeignKey(
        User,
        related_name="comments",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Comments"

    def __str__(self):
        return str(self.body)
