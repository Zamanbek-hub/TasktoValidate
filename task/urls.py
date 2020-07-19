from django.urls import path, include
from . import views
# from rest_framework import routers
# router = routers.DefaultRouter()


urlpatterns = [
    path('check',                views.index,            name='index'),
    # path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken')),
    # path('get/',                views.UserProfileViewset,            name='get'),

    path('user/<int:id>',
         views.GenericAPIView.as_view(), name='generic'),

]
