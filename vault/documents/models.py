from django.contrib.auth.models import User
from django.db import models


# Create your models here.

# CREATE MODEL TO STORE DOCUMENTS

class Documents(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=100, choices=(
    ('collage document', 'collage document'), ('government document', 'government document'),
    ('other document', 'other document')))
    name = models.CharField(max_length=100)
    document = models.ImageField(upload_to='images/')
    person_name = models.CharField(max_length=100)
    document_id = models.CharField(max_length=100)
    country = models.CharField(max_length=100, choices=(
    ('india', 'india'), ('america', 'america'), ('china', 'china'), ('bangladesh', 'bangladesh'),
    ('madhya pradesh', 'madhya pradesh'), ('assam', 'assam'), ('others', 'others')))
    is_legal = models.CharField(max_length=100, choices=(('legal', 'legal'), ('illegal', 'illegal'), ('both', 'both')))
    nominee=models.CharField(max_length=100)
    nominee_contact=models.CharField(max_length=100)
    type_doc=models.CharField(max_length=100,choices=(('file','file'),('list','list')))

