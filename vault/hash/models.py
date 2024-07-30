from django.contrib.auth.models import User
from django.db import models

# Create your models here.


# CREATE MODEL TO STORE PASSWORDS

class Passwords(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    your_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    type = models.CharField(
        max_length=100,
        choices=(
            ('instagram', 'Instagram'),
            ('facebook', 'Facebook'),
            ('twitter', 'Twitter'),
            ('google', 'Google'),
            ('other', 'Other')
        )
    )
    type_name = models.CharField(max_length=100)
    id_name = models.CharField(max_length=100)
    date_updated = models.DateTimeField(auto_now=True)
    created_date = models.DateTimeField(auto_now_add=True)  # Tracks when the password entry was created
    is_active = models.BooleanField(default=True)  # Indicates whether the password is active or not
    description = models.TextField(blank=True, null=True)  # Optional field for additional context
    notes = models.TextField(blank=True, null=True)  # Optional field for any additional notes

    def __str__(self):
        return self.id_name



