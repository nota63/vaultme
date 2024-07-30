from django.contrib.auth.models import User
from django.db import models

# Create your models here.


# CREATE CONTACT MODEL

class Cont(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    relation=models.CharField(max_length=100,choices=(('mother','mother'),('father','father'),('family','family'),('gf/bf','gf/bf'),('others','others')))
    contact=models.CharField(max_length=100)
    type=models.CharField(max_length=100,choices=(('important','important'),('less','less')))
    active=models.BooleanField(default=True)





