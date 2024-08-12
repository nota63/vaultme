from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import add_blog,view_blogs,delete_blog,edit_blog,view_your_blogs,analytics_view_blogs,analytics_view_blogs_user

urlpatterns = [

    path("add_blog/", add_blog, name='add_blog'),
    path("view_blogs/",view_blogs,name='view_blogs'),
    path('blogs/delete/<int:blog_id>/',delete_blog, name='delete_blog'),
    path('blogs/edit/<int:blog_id>/',edit_blog, name='edit_blog'),
    path("view_your_blogs/",view_your_blogs,name='view_your_blogs'),
    path("analytics_view_blogs/",analytics_view_blogs,name='analytics_view_blogs'),
    path("analytics_view_blogs_user/",analytics_view_blogs_user,name='analytics_view_blogs_user'),

]
