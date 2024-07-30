from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("add_task/",add_task,name='add_task'),
    path("delete_task/<int:task_id>/",delete_task,name='delete_task'),
    path('edit_task/<int:task_id>/', edit_task, name='edit_task'),
]