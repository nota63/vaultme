from django.contrib.auth.models import User
from django.db import models


# Create your models here.

# create models to take notes

class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    chapter = models.CharField(max_length=100)
    notes = models.CharField(max_length=1000000000)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return len(self.notes)


# create model to store e-books

class Ebooks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    ebook = models.FileField(upload_to='ebooks/')
    date = models.DateTimeField(auto_now=True)


# create model to post job openings

class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=10000)
    skills_required = models.CharField(max_length=1000)
    company = models.CharField(max_length=100)
    extra_details = models.CharField(max_length=10000)
    salary = models.CharField(max_length=100)
    image = models.ImageField(upload_to='jobs/')
    email = models.EmailField()

    def __str__(self):
        return f"{self.title} - {self.company}"


class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField()

    def __str__(self):
        return f"Application for {self.job.title} by {self.user.username}"


# Assignments models
class Assignments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    attachments = models.FileField(upload_to='assignments/')
    due_on = models.DateField()
    is_completed = models.BooleanField(default=False)
    listed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} -- {self.title}"


class Mark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignments, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)


class DoWork(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignments, on_delete=models.CASCADE)
    write = models.CharField(max_length=500000000)


class Attachments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignments, on_delete=models.CASCADE, related_name='attached')
    add_attachments = models.FileField(upload_to='add_attachments/')
    description = models.CharField(max_length=500000000)
    date_attached = models.DateTimeField(auto_now=True)


# model for create profiles

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    joined_VaultMe = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} Profile'


# create model to posts

class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pic = models.ImageField(upload_to='posts/', null=True, blank=True)
    date = models.DateTimeField(auto_now=True)


# model to save digital assets

class DigitalAssets(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    asset_name=models.CharField(max_length=100)
    asset=models.FileField(upload_to='assets/', null=True, blank=True)
    type=models.CharField(max_length=100,choices=(('PDf','PDF'),('Folder','Folder'),('File','File'),('Image','Image'),('Audio','Audio'),('Video','Video'),('Zip','Zip'),('Other','Other')))
    text=models.CharField(max_length=1000)
    date_added=models.DateTimeField(auto_now=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)






