from django.db import models
from django.contrib.auth.models import User

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
        # print("Model delete", UserProfile.avatar.name)

        # Overwrite delete method to delete img after delete Profile
        # but it turns out he himself deletes the photo from the folder without Overwrite
        self.avatar.delete(save=False)
        super(UserProfile, self).delete()
