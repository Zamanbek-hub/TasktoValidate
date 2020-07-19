from django.shortcuts import render
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

# Create your views here.


@api_view(['GET'])
def index(request):
    date = str(datetime.now())
    message = 'Colck in server is '
    print(Response(data=message+date, status=status.HTTP_200_OK))
    return Response(data=message+date, status=status.HTTP_200_OK)


class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin,
                     mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    lookup_field = 'id'

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    # IF we logout from Django
    # will be message like this in DjangoRestAdmin
    # {
    #     "detail": "Authentication credentials were not provided."
    # }

    # ListModelMixin

    # def validateImage(content):
    #     content_type = content.content_type.split('/')[0]
    #     print(content_type)
    #     print("Checkk")
    #     if content_type in settings.CONTENT_TYPES:
    #         if content.size > int(settings.MAX_UPLOAD_SIZE):
    #             return Response(('Please keep filesize under %s. Current filesize %s') % (
    #                 filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(content.size)), status=status.HTTP_400_BAD_REQUEST)

    #         # return Response('Success', status=status.HTTP_200_OK)
    #     else:
    #         return Response(('File type is not supported'), status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):

        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    # CreateModelMixin
    def post(self, request, id):

        return self.create(request)

    # UpdatedModelMixin
    def put(self, request, id=None):  # why none?
        print(request.data.get("avatar", None))

        return self.update(request, id)

    def delete(self, request, id):
        return self.destroy(request, id)
