from django.conf.urls import url
from shy.posts import views

urlpatterns = [
    # Home page
    url('^$', views.home, name='home'),

    # Signel post
    url('^post/(?P<uuid>[\w.@+-]+)/$', views.single_post, name='single_post'),
]
