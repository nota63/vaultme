from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from.views import store_passwords,view_passwords,delete_passwords,analytics_view_passwords


urlpatterns = [

 path("store_passwords/",store_passwords,name='store_passwords'),
 path("view_passwords/",view_passwords,name='view_passwords'),
 path("delete_passwords/<int:passwords_id>/",delete_passwords,name='delete_passwords'),
 path("analytics_view_passwords/",analytics_view_passwords,name='analytics_view_passwords'),

]