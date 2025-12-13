from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(null=True,blank=True)
    """allows a user A to follow user B without user B automatically following user A in return. """
    followers = models.ManyToManyField('self',symmetrical=False,related_name='following', blank=True)
 

