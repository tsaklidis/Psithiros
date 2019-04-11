from django.conf.urls import url
from shy.posts import views

urlpatterns = [
    # Home page
    url('^$', views.home, name='home'),

    # Signel post
    url('^post/(?P<uuid>[\w.@+-]+)/$', views.single_post, name='single_post'),

    # New post
    url('^new/$', views.new_post, name='new_post'),
]
