from typing import ClassVar
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db.models import EmailField
from django.db.models import ImageField
from django.db.models import BooleanField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator
from django.shortcuts import get_object_or_404
from .managers import UserManager


def user_image_location(instance, filename):
    return "{}/{}".format(
        str(instance.email)
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


class User(AbstractUser):
    """
    Default custom user model for Rhixe Scans Api.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    first_name = CharField(_("First Name of User"), blank=True, max_length=255)
    last_name = CharField(_("Last Name of User"), blank=True, max_length=255)
    email = EmailField(_("email address"), unique=True)
    username = CharField(_("User Name"), unique=True, max_length=255)
    images = ImageField(
        _("Images"),
        upload_to=user_image_location,
        validators=[
            ext_validator,
        ],
        blank=True,
    )
    is_superuser = BooleanField(_("Is superuser"), default=False)
    is_staff = BooleanField(_("Is staff"), default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects: ClassVar[UserManager] = UserManager()

    class Meta:
        verbose_name_plural = "Users"
        ordering = ["pk"]

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.pk:
            existing = get_object_or_404(User, pk=self.pk)
            if existing.images != self.images:
                existing.images.delete(save=False)

        super(User, self).save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})
