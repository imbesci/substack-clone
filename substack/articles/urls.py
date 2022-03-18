from django.urls import include, path, re_path
from . import views

app_name = 'articles'

urlpatterns = [
    re_path(r'^$', views.articles_authors, name="authors"),
    re_path(r'^genre/$', views.articles_genre, name='genre'),
    re_path(r'^drafts/$', views.view_drafts, name='drafts'),
    re_path(r'^create/$', views.create_article, name="create"),
    re_path(r'^(?P<slug>[\w-]+)/$', views.full_article, name='full'),
    re_path(r'^edit/(?P<key>[\d]+)/$', views.update_article, name='update' )
] 