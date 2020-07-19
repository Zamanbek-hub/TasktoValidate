from django.db import models
from django.contrib.auth.models import User
import os

# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    firstname = models.CharField('firstName', max_length=100, )
    lastname = models.CharField('lastName', max_length=100, )
    sex = models.BooleanField(blank=True)
    avatar = models.ImageField(upload_to='avatars', blank=True)
    email = models.EmailField('email', max_length=100)
    born = models.DateTimeField(null=True, blank=True)
    # asdsd = models.CharField('firstName', max_length=100, )

    def __str__(self):
        return str(self.user.username)

    def delete(self):
        # images = UserProfile.objects.filter(product=self)
        # for image in images:
        #     image.delete()
        # os.remove(UserProfile.avatar.pah)

        # print("Model delete", UserProfile.avatar.name)
        self.avatar.delete(save=False)
        super(UserProfile, self).delete()
