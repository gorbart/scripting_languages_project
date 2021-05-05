import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from apps.twitter_analyser.models import Hashtag
from apps.twitter_analyser.utils.plot_painter import PlotPainter
from apps.twitter_analyser.utils.twitter_api_pipeline import TwitterApiPipeline
from apps.twitter_analyser.views.utils import get_all_dates_for_user, handle_new_following


class QueryDateView(LoginRequiredMixin, View):
    """
    QueryDateView class is used to handle rendering index page of Twitter Analyser with contents retrieved from database for
    a given date related to a query which can be followed hashtag's text or followed profile's username.
    Attributes:
        - api_pipeline TwitterApiPipeline object with credentials assigned to this project
    """

    api_pipeline = TwitterApiPipeline()

    def get(self, request, year, month, day, query):
        """
        get method renders index.html with contents retrieved from database related to followed Hashtag and
        TwitterProfile instances chosen by passing hashtag's text or profile's username (if there is hashtag text passed
        - Profile is the first one alphabetically and vice versa) and saved on given date.
        :param day: day of searched date
        :param month: month of searched date
        :param year: year of searched date
        :param query: hashtag text or profile's username
        :param request: GET request
        :return: rendered index.html page with dictionary containing current date (here year/month/date parameters),
        list of dates application has been used, list of trending in the world hashtags retrieved from Twitter API,
        chart presenting their popularity, lists of hashtags and Twitter profiles followed by user, current hashtag (may
        be from query, otherwise alphabetically first), list of most popular posts related to it, chart presenting their
        statistics, current profile (may be from query, otherwise alphabetically first), list of most popular posts
        related to it and chart presenting their statistics
        """

        appuser = request.user.appuser
        users_hashtags = appuser.followed_hashtags.all()
        users_profiles = appuser.followed_profiles.all()

        trending_hashtags_from_db = Hashtag.objects.all()

        dates = list(set([hashtag.save_date for hashtag in trending_hashtags_from_db]))

        current_date = datetime.datetime(year, month, day)

        trending_hashtags = Hashtag.objects.filter(appuser__isnull=True).filter(save_date=current_date).distinct()

        if trending_hashtags:
            trending_hashtags_list = [trending_hashtag for trending_hashtag in trending_hashtags]

            trending_hashtags_list.sort(key=lambda hashtag: hashtag.tweet_volume, reverse=True)
            trending_hashtags_chart = PlotPainter.plot_hashtags(trending_hashtags_list)
        else:
            trending_hashtags_list = None
            trending_hashtags_chart = None

        if users_hashtags:
            current_hashtag = users_hashtags.filter(text=query)[0] if query[0] == '#' else users_hashtags[0]

            hashtags_tweets = current_hashtag.tweets.filter(save_date=current_date).distinct()

            hashtags_tweets_list = [hashtags_tweet for hashtags_tweet in hashtags_tweets]

            hashtags_tweets_list.sort(key=lambda tweet: (tweet.retweets, tweet.likes), reverse=True)
            hashtags_tweets_list = hashtags_tweets_list[:10]
            hashtags_tweets_chart = PlotPainter.plot_tweets(hashtags_tweets_list)
        else:
            current_hashtag = None
            hashtags_tweets_list = None
            hashtags_tweets_chart = None

        if users_profiles:
            current_profile = users_profiles.filter(username=query)[0] if query[0] != '#' else users_profiles[0]

            profiles_tweets = current_profile.tweet_set.filter(save_date=current_date).distinct()

            profiles_tweets_list = [profiles_tweet for profiles_tweet in profiles_tweets]

            profiles_tweets_list.sort(key=lambda tweet: (tweet.retweets, tweet.likes), reverse=True)
            profiles_tweets_list = profiles_tweets_list[:10]
            profiles_tweets_chart = PlotPainter.plot_tweets(profiles_tweets_list)
        else:
            current_profile = None
            profiles_tweets_list = None
            profiles_tweets_chart = None

        return render(request, 'twitter_analyser/index.html', {'current_date': current_date,
                                                               'dates': dates,
                                                               'trending_hashtags': trending_hashtags_list,
                                                               'trending_hashtags_chart': trending_hashtags_chart,
                                                               'users_hashtags': users_hashtags,
                                                               'users_profiles': users_profiles,
                                                               'current_hashtag': current_hashtag,
                                                               'hashtags_tweets': hashtags_tweets_list,
                                                               'hashtags_tweets_chart': hashtags_tweets_chart,
                                                               'current_profile': current_profile,
                                                               'profiles_tweets': profiles_tweets_list,
                                                               'profiles_tweets_chart': profiles_tweets_chart})

    def post(self, request, year, month, day, query):
        """
        post method is used to follow new hashtags and profiles
        :param query: query in view's url; ignored here
        :param day: day in view's url; ignored here
        :param month: month in view's url; ignored here
        :param year: year in view's url; ignored here
        :param request: POST request with demanded hashtag or profile username
        :return: redirection to index page
        """

        handle_new_following(request, self.api_pipeline)
        return redirect('twitter_analyser:index')
