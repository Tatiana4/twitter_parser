from django.db import models

# Create your models here.


class Tweet(models.Model):
    class Meta():
        db_table = 'Tweets'
    tweet_text = models.CharField(max_length=200)
    tweet_date = models.DateTimeField()
    tweet_username = models.CharField(max_length=50)


class User(models.Model):
    class Meta():
        db_table = 'Users'
    username = models.ForeignKey(Tweet)
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50, blank=True)
    friends = models.IntegerField()
    followers = models.IntegerField()
    description = models.CharField(max_length=200, blank=True)
    creation_date = models.DateField()
