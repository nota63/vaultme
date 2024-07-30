from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import add_person,view_persons,delete_persons,download_persons,analytics


urlpatterns = [

    path("add_person/",add_person,name='add_person'),
    path("view_persons/",view_persons,name='view_persons'),
    path('delete_persons/<int:person_id>/',delete_persons, name='delete_persons'),
    path('download_persons/',download_persons, name='download_persons'),
    path('analytics/',analytics,name='analytics'),

]
