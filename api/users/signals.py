from django.db.models.signals import pre_delete
from django.dispatch import receiver


@receiver(pre_delete, sender="users.User")
def server_delete_files(sender, instance, **kwargs):
    for field in instance._meta.fields:
        if field.name == "images":
            file = getattr(instance, field.name)
            if file:
                file.delete(save=False)
