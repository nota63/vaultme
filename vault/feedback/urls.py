from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [

   path("feedback/",feedback,name='feedback'),
   path("feed_done/",feed_done,name='feed_done'),


]