from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^users/$', views.users, name='user'),
    url(r'^users/(?P<arg_id>[0-9]+)/$', views.user_id, name="user_id"),
    url(r'^tags/$', views.tags, name='tag'),
    url(r'^tags/(?P<arg_id>[0-9]+)/$', views.tag_id, name="tag_id"),
    url(r'^articles/$', views.articles, name='article'),
    url(r'^articles/(?P<arg_id>[0-9]+)/$', views.article_id, name="article_id"),
]
