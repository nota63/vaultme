from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Pdf(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='pdfs')
    uploaded_at = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=100, choices=(('important', 'important'), ('less', 'less')))

    # New fields
    description = models.TextField(blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=100, choices=[
        ('personal', 'Personal'),
        ('work', 'Work'),
        ('study', 'Study'),
        ('other', 'Other')
    ], default='personal')
    size = models.PositiveIntegerField(blank=True, null=True)  # Size in bytes

    def __str__(self):
        return self.name

