from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [

 path("reviews/",reviews,name='reviews'),
 path("view_reviews/",view_reviews,name='view_reviews'),
 path("collaborate/",collaborate,name='collaborate'),
 path("success/",success,name='success'),
 path("projects/",projects,name='projects'),
 path("view_projects/",view_projects,name='view_projects'),
 path("delete_projects/<int:project_id>/",delete_projects,name='delete_projects'),
 path("analytics_view_projects",analytics_view_projects,name='analytics_view_projects'),
 path("code_editor/",code_editor,name='code_editor'),
 path("share/",share,name='share'),
 path("view_shares/",view_shares,name='view_shares'),
 path('shares/delete/<int:pk>/', delete_project_share, name='delete_project_share'),
 path('projects/<int:pk>/add_comment/', add_comment, name='add_comment'),
 path('comments/<int:comment_pk>/add_reply/',add_reply, name='add_reply'),
 path("own_projects/",own_projects,name='own_projects'),
 path("delete_own/<int:projects2_id>/",delete_own,name='delete_own'),
 path("pyjokes_view/",pyjokes_view,name='pyjokes_view'),
 path("invite/",invite,name='invite'),




]