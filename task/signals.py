import os
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete
from django.contrib.auth.models import User
from .models import UserProfile


def _delete_file(path):
    """ Deletes file from filesystem. """
    # if os.path.isfile(path):
    print("delete ", path)
    # os.remove(path)


@receiver(pre_save, sender=UserProfile)
def update_file(sender, instance, **kwargs):
    """Deletes image files on `pre_save` """
    print("update")

    """
    Delete old photo when uploaded new photo
    I tried delete by OS in _delete_file() but this didn't work, may be from unicode(Russian) or from pre_save as so PATH shows  of new uploaded IMG

    """
    # if created == False:
    if not instance._state.adding:
        pass
        # instance.avatar.delete()
        # _delete_file(instance.avatar.delete)
        print("Its update")
    else:
        print("Its insert")


@receiver(pre_delete, sender=UserProfile)
def delete_file(sender, instance, **kwargs):
    """ Deletes image files on `pre_save` """
    print("delete")
    # if created == False:

    _delete_file(instance.avatar.name)
