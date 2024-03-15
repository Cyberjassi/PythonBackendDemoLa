from django.db import models

#this is inbulit user by django-
from django.contrib.auth.models import AbstractUser
#import manager from manager.py file-
from app.manager import UserManager 

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=16)
    bio = models.CharField(max_length=164, null=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    

class Post(models.Model):
    user = models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='post_images/',null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class PostLike(models.Model):
    post = models.ForeignKey(Post,null=False,on_delete=models.CASCADE)
    user = models.ForeignKey(User,null=False,on_delete=models.CASCADE)

    class Meta:
        # it means one user do one like in post only
        unique_together = (("post","user"),)

class Comment(models.Model):
    comment_text = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=False, on_delete=models.CASCADE) 

class UserFollow(models.Model):
    user = models.ForeignKey(User,null=False,on_delete=models.CASCADE,related_name="src_follow")
    follows = models.ForeignKey(User,max_length=100,null=False,on_delete=models.CASCADE,related_name="des_follow")