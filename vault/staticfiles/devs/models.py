from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.

# model to get devs help or queries / reviews

class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pros = models.CharField(max_length=10000)
    cons = models.CharField(max_length=10000)
    suggestion = models.CharField(max_length=50000)
    date_posted = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f"review from {self.user}"


# CREATE MODEL TO SAVE COLLABORATION DATA

class Collaborate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=50)
    email = models.EmailField()
    specialized_skills = models.CharField(max_length=500)
    resume = models.FileField(upload_to='pdfs/')
    applying_for = models.CharField(max_length=500, choices=(
        ('Backend', 'Backend'), ('Frontend', 'Frontend'), ('Database', 'Database'), ('APIs', 'APIs'), ('SEO', 'SEO'),
        ('Logos', 'Logos')))
    date_applied = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Freelance application from {self.user}"


# model to store projects

class Projects(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=200)
    requirements = models.CharField(max_length=1000)
    what_does = models.CharField(max_length=500)
    files = models.FileField(upload_to='projects/')
    date_added = models.DateTimeField(auto_now=True)


# for code editor
class CodeSnippet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    code = models.TextField()
    language = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# model for conversation
class ProjectShare(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    description = models.CharField(max_length=10000)
    image = models.ImageField(upload_to='images/')
    live_link = models.URLField()
    date = models.DateTimeField(auto_now=True)


class Comment_dev(models.Model):
    project = models.ForeignKey(ProjectShare, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.project.name}'


class Reply_dev(models.Model):
    comment = models.ForeignKey(Comment_dev, related_name='replies', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Reply by {self.user.username} on comment {self.comment.id}'

    # model to save skillls


class Skills(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='skills/')

    def __str__(self):
        return self.user



