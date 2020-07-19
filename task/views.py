from django.shortcuts import render
from django.urls import reverse_lazy
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from datetime import datetime
from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.dispatch import receiver
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def auth(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        # return HttpResponse(username)

        check_if_user_exists = User.objects.filter(
            username=username).exists()

        print(check_if_user_exists)

        if check_if_user_exists:

            print("gjlkjh;lj;")
            # a = login(username="+7 (708)-050-52-67", password="just")
            # print(a)
            profile = authenticate(
                username=username, password=password)

            # a = login(username="+7 (708)-050-52-67", password="just")
            # print(user)
            if profile is not None:
                # print("We are here")
                # profile = UserProfile.objects.get(user=user)
                login(request, profile)

                print("Logined")
                return HttpResponseRedirect(reverse_lazy('list',))

            else:
                return Response("Invalid login or Password", status=status.HTTP_400_BAD_REQUEST)

    return render(request, 'task/auth.html')


@ api_view(['GET'])
def index(request):
    date = str(datetime.now())
    message = 'Clock in server is '
    print(Response(data=message+date, status=status.HTTP_200_OK))
    return Response(data=message+date, status=status.HTTP_200_OK)


# def _delete_file(path):
#     """ Deletes file from filesystem. """
#     if os.path.isfile(path):
#         print("delete")
#         os.remove(path)


# @receiver(models.signals.post_delete, sender=UserProfile)
# def delete_file(sender, instance, *args, **kwargs):
#     """ Deletes image files on `post_delete` """
#     if instance.avatar:
#         _delete_file(instance.image.path)


def validateImage(content):
    content_type = content.content_type.split('/')[0]
    print(content_type)
    print("Checkk")
    if content_type in settings.CONTENT_TYPES:
        if content.size > int(settings.MAX_UPLOAD_SIZE):
            return Response(('Please keep filesize under %s. Current filesize %s') % (
                filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content.size)), status=status.HTTP_400_BAD_REQUEST)

        # return Response('Success', status=status.HTTP_200_OK)
    else:
        return Response(('File type is not supported'), status=status.HTTP_400_BAD_REQUEST)


class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
                     mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    lookup_field = 'id'

    authentication_classes = [SessionAuthentication]
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # IF we logout from Django
    # will be message like this in DjangoRestAdmin
    # {
    #     "detail": "Authentication credentials were not provided."
    # }

    # ListModelMixin

    # @classmethod

    def get(self, request, id=None):

        if id:
            return self.retrieve(request)
        else:
            print(type(id))
            return self.list(request)

    # CreateModelMixin
    def post(self, request, id):

        try:
            content = request.data.get("avatar", None)
            # print("Contene = " + content)
            content_type = content.content_type.split('/')[0]
            print(content_type)
            print("Checkk")

            if content_type in settings.CONTENT_TYPES:
                if content.size > int(settings.MAX_UPLOAD_SIZE):
                    return Response(('Please keep filesize under %s. Current filesize %s') % (
                        filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content.size)), status=status.HTTP_400_BAD_REQUEST)

                # return Response('Success', status=status.HTTP_200_OK)
            else:
                return Response(('File type is not supported'), status=status.HTTP_400_BAD_REQUEST)

            return self.create(request)
        except AttributeError:
            return Response(('Something went wrong \n May be image did not choose'), status=status.HTTP_400_BAD_REQUEST)

    # UpdatedModelMixin

    def put(self, request, id=None):  # why none?
        try:
            # return HttpResponse(request.kwargs)
            content = request.data.get("avatar", None)
            # print("Contene = " + content)
            content_type = content.content_type.split('/')[0]
            print(content_type)
            print("Checkk")

            if content_type in settings.CONTENT_TYPES:
                if content.size > int(settings.MAX_UPLOAD_SIZE):
                    return Response(('Please keep filesize under %s. Current filesize %s') % (
                        filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content.size)), status=status.HTTP_400_BAD_REQUEST)

                # return Response('Success', status=status.HTTP_200_OK)
            else:
                return Response(('File type is not supported'), status=status.HTTP_400_BAD_REQUEST)

            return self.update(request, id)
        except AttributeError:
            return Response(('Something went wrong \n May be image did not choose'), status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        return self.destroy(request, id)


@ api_view(('GET',))
def article_detail(request):
    try:
        userProfiles = UserProfile.objects.all()

    except Article.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserProfileSerializer(userProfiles, many=True)
        # serializer = ArticleSerializerModel(
        #     articles, many=True)
        return Response(serializer.data)
