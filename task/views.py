from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
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

from django.contrib.auth import authenticate, login, logout

# Create your views here.


def auth(request):
    # if user want to login
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        check_if_user_exists = User.objects.filter(
            username=username).exists()

        print(check_if_user_exists)

        # login user
        if check_if_user_exists:
            try:
                profile = authenticate(
                    username=username, password=password)

                if profile is not None:
                    login(request, profile)
                    print("Logined")
                    return HttpResponseRedirect(reverse_lazy('profileListLinks',))

                else:
                    return HttpResponse("Invalid login or Password", status=status.HTTP_400_BAD_REQUEST)

            except:
                return HttpResponse("Invalid login or Password", status=status.HTTP_400_BAD_REQUEST)

    return render(request, 'task/auth.html')


def profileListLinks(request):
    userProfiles = UserProfile.objects.all()
    return render(request, 'task/profileListLinks.html', {'userProfiles': userProfiles})


def log_out(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('auth'))


# Testing Drf
@ api_view(['GET'])
def index(request):
    date = str(datetime.now())
    message = 'Clock in server is '
    print(Response(data=message+date, status=status.HTTP_200_OK))
    return Response(data=message+date, status=status.HTTP_200_OK)


class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
                     mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    lookup_field = 'id'

    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    # IF we logout from Django
    # will be message like this in DjangoRestAdmin
    # {
    #     "detail": "Authentication credentials were not provided."
    # }

    # ListModelMixin
    def get(self, request, id=None):

        if id:
            return self.retrieve(request)
        else:
            print(type(id))
            return self.list(request)

    # CreateModelMixin
    def post(self, request, id):
        """
        Why i duplicate below code to check upload Image size, in (post, update) ?
        I didn't find decorator or way to insert this code in this class like def, (terminal didn't see in class)
        I tried output code outside the class, but in this case Responces will be ignoring as so this would return function,
        then to process responce from function i have to duplicate process
        That's why i just duplicate below code in 2 place

        """
        try:
            content = request.data.get("avatar", None)
            content_type = content.content_type.split('/')[0]

            """Check to image type and size"""
            if content_type in settings.CONTENT_TYPES:
                if content.size > int(settings.MAX_UPLOAD_SIZE):
                    return Response(('Please keep filesize under %s. Current filesize %s') % (
                        filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content.size)), status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response(('File type is not supported'), status=status.HTTP_400_BAD_REQUEST)

            return self.create(request)
        except AttributeError:  # if img field will be empty
            return Response(('Something went wrong \n May be image did not choose'), status=status.HTTP_400_BAD_REQUEST)

    # UpdatedModelMixin
    def put(self, request, id=None):  # why none?
        try:

            content = request.data.get("avatar", None)
            content_type = content.content_type.split('/')[0]

            """Check to image type and size"""
            if content_type in settings.CONTENT_TYPES:
                if content.size > int(settings.MAX_UPLOAD_SIZE):
                    return Response(('Please keep filesize under %s. Current filesize %s') % (
                        filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content.size)), status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response(('File type is not supported'), status=status.HTTP_400_BAD_REQUEST)

            return self.update(request, id)
        except AttributeError:  # if img field will be empty
            return Response(('Something went wrong \n May be image did not choose'), status=status.HTTP_400_BAD_REQUEST)

    # DestroyModelMixin
    def delete(self, request, id):
        return self.destroy(request, id)


# to show all UserProfiles in DRF
@ api_view(('GET',))
def article_detail(request):
    try:
        userProfiles = UserProfile.objects.all()

    except Article.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserProfileSerializer(userProfiles, many=True)
        return Response(serializer.data)
