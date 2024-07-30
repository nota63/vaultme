from django.contrib import admin
from .models import Feedback

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user','comments',)
    list_filter = ('user',)
    search_fields = ('user',)


# Register your models here.
admin.site.register(Feedback)