from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE) #CASCADE means if a user is deleted all their associated posts are also deleted
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', args=[self.pk])


class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name = 'comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self):
        return f"comment by {self.author}"


    
