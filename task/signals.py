import os
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete
from django.contrib.auth.models import User
from .models import UserProfile


def _delete_file(path):
    """ Deletes file from filesystem. """
    # if os.path.isfile(path):
    # indexes = indexes.translate({ord(']'): None})
    path = "C:/Users/ЗФманбек/Desktop/projectTasktoWork/TasktoValidate/main/task/media/avatars/DSC_0740.JPG"
    print("delete ", path)
    # os.remove(path)


@receiver(pre_save, sender=UserProfile)
def update_file(sender, instance, **kwargs):
    """ Deletes image files on `pre_save` """
    print("TO Update")
    # if created == False:
    if not instance._state.adding:
        print("Its update", instance)
        instance.avatar.delete()
        # _delete_file(instance.avatar.delete)
    else:
        print("Its insert")


@receiver(pre_delete, sender=UserProfile)
def delete_file(sender, instance, **kwargs):
    """ Deletes image files on `pre_save` """
    print("TO delete")
    # if created == False:
    # if not instance._state.adding:
    print("Its delete", instance.avatar.name)
    _delete_file(instance.avatar.name)
    # else:
    #     print("Its insert")
