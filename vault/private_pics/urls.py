from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from.views import store_pics,view_pis,download_images,delete_pics,analytics_view_private


urlpatterns = [

    path("store_pics/",store_pics,name='store_pics'),
    path('view_pis/',view_pis,name='view_pis'),
    path("download_images/",download_images,name='download_images'),
    path("delete_pics/<int:pic_id>/",delete_pics,name='delete_pics'),
    path("analytics_view_private/",analytics_view_private,name='analytics_view_private'),
]