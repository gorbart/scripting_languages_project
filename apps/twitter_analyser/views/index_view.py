from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from apps.twitter_analyser.models import Hashtag
from apps.twitter_analyser.utils.plot_painter import PlotPainter
from apps.twitter_analyser.utils.twitter_api_pipeline import TwitterApiPipeline
from apps.twitter_analyser.views.utils import handle_new_following


class IndexView(LoginRequiredMixin, View):
    """
    IndexView class is used to handle rendering index page of Twitter Analyser with contents retrieved from Twitter API.
    It also saves the contents in database.
    Attributes:
        - api_pipeline TwitterApiPipeline object with credentials assigned to this project
    """

    api_pipeline = TwitterApiPipeline()

    def get(self, request):
        """
        get method renders index.html with contents retrieved from Twitter API and default (first alphabetically)
        followed Hashtag and TwitterProfile instances.
        :param request: GET request
        :return: rendered index.html page with dictionary containing current date (here None as we don't retrieve
        anything from database; only from Twitter API), list of dates application has been used, list of trending in the
        world hashtags retrieved from Twitter API, chart presenting their popularity, lists of hashtags and Twitter
        profiles followed by user, current hashtag (first alphabetically), list of most popular posts related to it,
        chart presenting their statistics, current profile (first alphabetically), list of most popular posts related to
        it and chart presenting their statistics
        """

        appuser = request.user.appuser
        users_hashtags = appuser.followed_hashtags.all()
        users_profiles = appuser.followed_profiles.all()

        trending_hashtags_from_db = Hashtag.objects.all()

        dates = list(set([hashtag.save_date for hashtag in trending_hashtags_from_db]))

        trending_hashtags = self.api_pipeline.get_top_hashtags_worldwide()
        trending_hashtags.sort(key=lambda hashtag: hashtag.tweet_volume, reverse=True)
        trending_hashtags_chart = PlotPainter.plot_hashtags(trending_hashtags)

        for trending_hashtag in trending_hashtags:
            if trending_hashtag not in trending_hashtags_from_db:
                trending_hashtag.save()

        if users_hashtags:
            current_hashtag = users_hashtags[0]

            current_hashtag_saved_tweets = current_hashtag.tweets.all()

            hashtags_tweets = self.api_pipeline.get_recent_tweets_for_hashtag(current_hashtag.text, how_many=5)

            for hashtags_tweet in hashtags_tweets:
                if hashtags_tweet not in current_hashtag_saved_tweets:
                    hashtags_tweet.save()
                    current_hashtag.tweets.add(hashtags_tweet)

            current_hashtag.save()

            hashtags_tweets.sort(key=lambda tweet: (tweet.retweets, tweet.likes), reverse=True)
            hashtags_tweets_chart = PlotPainter.plot_tweets(hashtags_tweets)
        else:
            current_hashtag = None
            hashtags_tweets = None
            hashtags_tweets_chart = None

        if users_profiles:
            current_profile = users_profiles[0]

            current_profile_saved_tweets = current_profile.tweet_set.all()

            profiles_tweets = self.api_pipeline.get_recent_tweets_for_author(current_profile.username, how_many=5)

            for profiles_tweet in profiles_tweets:
                if profiles_tweet not in current_profile_saved_tweets:
                    profiles_tweet.save()
                    current_profile.tweet_set.add(profiles_tweet)

            current_profile.save()

            profiles_tweets.sort(key=lambda tweet: (tweet.retweets, tweet.likes), reverse=True)
            profiles_tweets_chart = PlotPainter.plot_tweets(profiles_tweets)
        else:
            current_profile = None
            profiles_tweets = None
            profiles_tweets_chart = None

        return render(request, 'twitter_analyser/index.html', {'current_date': None,
                                                               'dates': dates,
                                                               'trending_hashtags': trending_hashtags,
                                                               'trending_hashtags_chart': trending_hashtags_chart,
                                                               'users_hashtags': users_hashtags,
                                                               'users_profiles': users_profiles,
                                                               'current_hashtag': current_hashtag,
                                                               'hashtags_tweets': hashtags_tweets,
                                                               'hashtags_tweets_chart': hashtags_tweets_chart,
                                                               'current_profile': current_profile,
                                                               'profiles_tweets': profiles_tweets,
                                                               'profiles_tweets_chart': profiles_tweets_chart})

    def post(self, request):
        """
        post method is used to follow new hashtags and profiles
        :param request: POST request with demanded hashtag or profile username
        :return: redirection to index page
        """

        handle_new_following(request, self.api_pipeline)
        return redirect('twitter_analyser:index')
