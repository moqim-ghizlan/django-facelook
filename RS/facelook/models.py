from django.db import models
from datetime import datetime, timedelta, date
from django.utils.html import format_html
from django.template.defaultfilters import date as django_date
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    first_name = models.CharField(max_length=150, null=False)
    last_name = models.CharField(max_length=150, null=False)
    email = models.EmailField(max_length=254, null=False, unique=True)
    bio = models.CharField(max_length=150, null=False,
                           default="Pas encore de bio...")
    image = models.ImageField(default="pngegg.png")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Topic(models.Model):
    title = models.CharField(max_length=150, null=False)
    text = models.TextField(max_length=1024, null=False)
    date = models.DateTimeField(auto_now_add=True, editable=False)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="topics")

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = ['-date']


class Post(models.Model):
    # text = models.CharField(max_length=150, null=False )
    text = models.TextField(max_length=1024, null=False )
    date = models.DateTimeField(auto_now_add=True, editable=False)
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE, related_name="posts")
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return f'text:{self.text}'

    class Meta:
        ordering = ['-date']


class Like(models.Model):
    value = models.BooleanField(default=True)  # True = Like, False = dislike
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return f'Post=<<{self.post}>>::value=<<{self.value}>>'


class Fallowing(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="fallowing")
    fallower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="fallower")

    def __str__(self):
        return f'[{self.user}] is fallowing [{self.fallower}]'
