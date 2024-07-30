"""
URL configuration for vault project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from vault import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.main,name='main'),
    path('accounts/', include('accounts.urls')),
    path("add_contact/",include('cont.urls')),
    path("add_person/",include('person.urls')),
    path("store_documents/",include('documents.urls')),
    path("store_pics/",include('private_pics.urls')),
    path("store_pdfs/",include('pdf.urls')),
    path("store_passwords/",include('hash.urls')),
    path("add_blog",include('disc.urls')),
    path("developer_platform/",views.developer_platform,name='developer_platform'),
    path("reviews/",include('devs.urls')),
    path("about/",views.about,name='about'),
    path("shutdown/",views.shutdown,name='shutdown'),
    path('system_info/', views.system_info_view, name='system_info'),
    path("task_manager/",views.task_manager,name='task_manager'),
    path("add_task/",include('task.urls')),
    path("feedback/",include('feedback.urls')),





]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)