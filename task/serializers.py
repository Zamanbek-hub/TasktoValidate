from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.models import User


class UserSerializerModel(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ('id', 'username', 'password',)


class UserProfileSerializer(serializers.ModelSerializer):

    # nested Serializer
    # user = UserSerializerModel(many=False, read_only=True)

    class Meta:

        model = UserProfile
        fields = ('user', 'firstname', 'lastname',
                  'sex', 'avatar', 'email', 'born',)
