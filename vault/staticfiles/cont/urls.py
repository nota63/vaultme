from django.contrib import admin
from django.urls import path, include
from .views import add_contact, view_contacts, delete_contact, download_contacts,analytics_view

urlpatterns = [

    path("add_contact/",add_contact,name='add_contact'),
    path("view_contacts/",view_contacts,name='view_contacts'),
    path('delete_contact/<int:cont_id>/', delete_contact, name='delete_contact'),
    path('download_contacts/', download_contacts, name='download_contacts'),
    path("analytics_view/",analytics_view,name='analytics_view'),



]
