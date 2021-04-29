from django.contrib.auth.models import User
from django.db import models

from apps.twitter_analyser.models import TwitterProfile, Hashtag


class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followed_profiles = models.ManyToManyField(TwitterProfile)
    followed_hashtags = models.ManyToManyField(Hashtag)
