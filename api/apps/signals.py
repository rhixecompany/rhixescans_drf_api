from django.db.models.signals import pre_delete
from django.dispatch import receiver


@receiver(pre_delete, sender="apps.ComicImagesItem")
def server_delete_files(sender, instance, **kwargs):
    for field in instance._meta.fields:
        if field.name == "image":
            file = getattr(instance, field.name)
            if file:
                file.delete(save=False)


@receiver(pre_delete, sender="apps.ChapterImagesItem")
def server_delete_files(sender, instance, **kwargs):
    for field in instance._meta.fields:
        if field.name == "image":
            file = getattr(instance, field.name)
            if file:
                file.delete(save=False)
