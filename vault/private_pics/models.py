from django.contrib.auth.models import User
from django.db import models

# Create your models here.

# CREATE MODEL TO STORE PRIVATE PICS


from django.conf import settings

class Private(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)  # Optional field for additional details
    date_created = models.DateTimeField(auto_now_add=True)  # Automatically set the date when the record is created
    category = models.CharField(max_length=100, choices=[
        ('personal', 'Personal'),
        ('work', 'Work'),
        ('vacation', 'Vacation'),
        ('other', 'Other')
    ], default='personal')
    tags = models.CharField(max_length=255, blank=True, null=True)  # Comma-separated tags or keywords
    size = models.PositiveIntegerField(blank=True, null=True)  # Size in bytes
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the User model

    def __str__(self):
        return self.name