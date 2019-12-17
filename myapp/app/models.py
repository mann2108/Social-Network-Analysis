from django.db import models
import random

class Tweeter(models.Model):
    user = models.ManyToManyField('self',symmetrical=False, through='Relationship')
    name = models.CharField(default='',max_length=30)
    user_name = models.CharField(default='',max_length=30)
    GENDER_CHOICES = (('M','Male'),('F','Female'),('O','Other'))
    gender = models.CharField(default='M',max_length=1,choices=GENDER_CHOICES)
    email = models.CharField(default='',max_length=100)
    password = models.CharField(default='',max_length=100)
    profile_pic_path = models.CharField(default='img.jpg',max_length=30)
    created_date = models.DateTimeField(auto_now_add=True, blank=True)

class Relationship(models.Model):
    who = models.ForeignKey(Tweeter,on_delete=models.CASCADE, related_name="who")
    whom = models.ForeignKey(Tweeter,on_delete=models.CASCADE, related_name="whom")
    friendship_date = models.DateTimeField(auto_now_add=True, blank=True)

class Post(models.Model):
    who = models.ForeignKey(Tweeter,on_delete=models.CASCADE,related_name="author")
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    file_name = models.CharField(default='',max_length=100)
    published_date = models.DateTimeField(auto_now_add=True, blank=True)


class HistoryOfPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post")
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    track_day = models.IntegerField(default=0)