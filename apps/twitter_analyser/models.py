from django.db import models

from apps.users.models import AppUser


class TwitterProfile(models.Model):
    """
    Class TwitterProfile is used to store Twitter users, who are followed by project's users.
    Attributes:
        - profile_id - id given to the user by Twitter
        - username - username connected with profile on Twitter
        - save_date - indicates when this TwitterProfile has been saved to database
    TwitterProfile is in relationships with Tweet (One-To-Many as each Tweet has only one author) and AppUser
    (Many-To-Many as every project user may follow several TwitterProfiles and they can be followed by several users).
    """

    profile_id = models.CharField(max_length=30)
    username = models.CharField(max_length=30)
    save_date = models.DateField()
    appuser = models.ForeignKey(AppUser, on_delete=models.CASCADE)

    def __repr__(self):
        return f"Twitter profile {self.username} with id {self.profile_id}"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if isinstance(other, TwitterProfile):
            return self.profile_id == other.profile_id or self.username == other.username
        return False

    def __hash__(self):
        return hash(self.username)

    class Meta:
        ordering = ['username', 'profile_id']


class Tweet(models.Model):
    """
    Class Tweet is used to store Tweets, which are followed by project's users or which are related to followed
    hashtags.
    Attributes:
        - tweet_id - id given to the Tweet by Twitter
        - creation_date - indicates when this Tweet has been posted
        - save_date - indicates when this Tweet has been saved to database
        - text - Tweet's text
        - retweets, likes - integers indicating how many retweets, likes or responses did the Tweet get
    Tweet is in relationships with TwitterProfile (Many-To-One as each Tweet has only one author) and Hashtag
    (Many-To-Many as every Tweet may have several Hashtags and they can be related to by several Tweets).
    """

    tweet_id = models.CharField(max_length=30)
    creation_date = models.DateField()
    save_date = models.DateField()
    text = models.CharField(max_length=500)
    retweets = models.IntegerField()
    likes = models.IntegerField()
    author = models.ForeignKey(TwitterProfile, blank=True, null=True, on_delete=models.SET_NULL)

    def __repr__(self):
        res_str = f"{self.text}. Posted on {self.creation_date}"
        if self.author:
            res_str += f" by {self.author.username}"
        return res_str

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if isinstance(other, Tweet):
            return self.tweet_id == other.tweet_id or self.text == other.text
        return False

    def __hash__(self):
        return hash(self.text)

    class Meta:
        ordering = ['creation_date', 'save_date', 'tweet_id']


class Hashtag(models.Model):
    """
    Class Hashtag is used to store Hashtags, which are followed by project's users.
    Attributes:
        - save_date - indicates when this Hashtag has been saved to database
        - text - Hashtag's text
        - tweet_volume - integer indicating how many times was this Hashtag used
    Hashtag is in relationships with Tweet (Many-To-Many as every Tweet may have several Hashtags and they can be
    related to by several Tweets).
    """

    save_date = models.DateField()
    text = models.CharField(max_length=50)
    tweet_volume = models.IntegerField(blank=True, null=True)
    tweets = models.ManyToManyField(Tweet)
    appuser = models.ForeignKey(AppUser, blank=True, null=True, on_delete=models.SET_NULL)

    def __repr__(self):
        return f"{self.text} used by {self.tweet_volume} tweets"

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        if isinstance(other, Hashtag):
            return self.text == other.text
        return False

    def __hash__(self):
        return hash(self.text)

    class Meta:
        ordering = ['save_date', 'text']
