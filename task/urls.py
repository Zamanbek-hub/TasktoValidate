from django.urls import path, include
from . import views


urlpatterns = [
    path('check',                views.index,            name='index'),
    path('',                views.auth,            name='auth'),
    path('log_out',      views.log_out,             name='log_out'),

    path('profileListLinks',
         views.profileListLinks, name='profileListLinks'),

    path('<int:id>',
         views.GenericAPIView.as_view(), name='generic'),

    path('list',
         views.article_detail, name='list'),

]
