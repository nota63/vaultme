from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Feedback(models.Model):
    CATEGORY_CHOICES = [
        ('bug', 'Bug Report'),
        ('feature', 'Feature Request'),
        ('general', 'General Feedback'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    rating = models.IntegerField(default=0)
    comments = models.TextField()
    file = models.FileField(upload_to='feedback_files/', null=True, blank=True)
    anonymous = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username if self.user else "Anonymous"} - {self.category}'