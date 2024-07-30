from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from.views import store_pdfs,view_pdfs,delete_pdfs,download_all_pdfs,pdf_analytics

urlpatterns = [

 path("store_pdfs/",store_pdfs,name='store_pdfs'),
 path("view_pdfs/",view_pdfs,name='view_pdfs'),
 path("delete_pdfs/<int:pdf_id>/",delete_pdfs,name='delete_pdfs'),
 path("download_all_pdfs/",download_all_pdfs,name='download_all_pdfs'),
 path("pdf_analytics/",pdf_analytics,name='pdf_analytics'),

]