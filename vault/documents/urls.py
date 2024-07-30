from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import store_documents,view_documents,download_documents,delete_documents,analytics_view_doc,guide

urlpatterns = [
    path("store_documents/",store_documents,name='store_documents'),
    path("view_documents/",view_documents,name='view_documents'),
    path("download_documents/",download_documents,name='download_documents'),
    path("delete_documents/<int:doc_id>/",delete_documents,name='delete_documents'),
    path("analytics_view_doc/",analytics_view_doc,name='analytics_view_doc'),
    path("guide/",guide,name='guide'),

]