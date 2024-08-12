from django.contrib import admin
from .models import Job, JobApplication,Assignments,Profile


class JobApplicationAdmin(admin.ModelAdmin):
    list_filter = ('job', 'user',)
    search_fields = ('job',)
    list_display = ('user', 'job',)


# Register your models here.
admin.site.register(Job)
admin.site.register(JobApplication, JobApplicationAdmin)
admin.site.register(Assignments)
admin.site.register(Profile)
