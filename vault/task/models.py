from django.contrib.auth.models import User
from django.db import models

# Create your models here.


# create model to store tasks

class Task(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    task_name=models.CharField(max_length=1000)
    category=models.CharField(max_length=1000,choices=(('Personal','Personal'),('Work','Work'),('Others','Others')))
    important=models.BooleanField(default=False)
    description=models.CharField(max_length=5000)
    date_to_accomplish=models.DateField()
    date_added=models.DateTimeField(auto_now=True)





