from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include(('shy.posts.urls', 'posts'), namespace='posts')),
    path('admin/', admin.site.urls),
]
