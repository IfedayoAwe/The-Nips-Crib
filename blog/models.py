from django.db import models
from django.utils import timezone
from users.models import User

class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=5000)
    date_posted = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'