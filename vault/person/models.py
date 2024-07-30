from django.contrib.auth.models import User
from django.db import models


# Create your models here. to store persons data

class Person(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    connection = models.CharField(max_length=100, choices=(
    ('brother', 'brother'), ('family member', 'family member'), ('stranger', 'stranger'), ('special', 'special'),
    ('freind', 'freind'), ('other', 'other')))
    social_id = models.CharField(max_length=200)
    type = models.CharField(max_length=100, choices=(
    ('instagram', 'instagram'), ('facebook', 'facebook'), ('twitter', 'twitter'), ('other','other')))
    special_name=models.CharField(max_length=100)

    def __str__(self):
        return self.name





