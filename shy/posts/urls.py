from django.conf.urls import url
from shy.posts import views

urlpatterns = [
    # Home page
    url('^$', views.home, name='home'),

    # Signel post
    url('^whisper/(?P<uuid>[\w.@+-]+)/$', views.single_post, name='single_post'),

    # search for posts
    url('^search/$', views.search, name='search'),

    # Info page
    url('^info/$', views.info, name='info'),

    # New post
    url('^new/whisper/$', views.new_post, name='new_post'),
]
