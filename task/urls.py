from django.urls import path, include
from . import views
# from rest_framework import routers
# router = routers.DefaultRouter()


urlpatterns = [
    path('check',                views.index,            name='index'),
    # path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.authtoken')),
    # path('get/',                views.UserProfileViewset,            name='get'),

    path('',                views.auth,            name='auth'),

    path('<int:id>',
         views.GenericAPIView.as_view(), name='generic'),

    # if user/<int:id> image doesn't show ('Page not found')
    # False url


]
