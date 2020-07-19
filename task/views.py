from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.


@api_view(['GET'])
def index(request):
    date = str(datetime.now())
    message = 'Colck in server is '
    print(Response(data=message+date, status=status.HTTP_200_OK))
    return Response(data=message+date, status=status.HTTP_200_OK)
