import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from apps.twitter_analyser.models import Hashtag
from apps.twitter_analyser.utils.plot_painter import PlotPainter
from apps.twitter_analyser.utils.twitter_api_pipeline import TwitterApiPipeline


class IndexView(LoginRequiredMixin, View):
    api_pipeline = TwitterApiPipeline()

    def get(self, request):
        appuser = request.user.appuser
        users_hashtags = appuser.followed_hashtags.all()
        users_profiles = appuser.followed_profiles.all()

        hashtag_dates = [hashtag.save_date for hashtag in users_hashtags]
        profile_dates = [profile.save_date for profile in users_profiles]
        hashtag_tweet_dates = [tweet.save_date for hashtag in users_hashtags for tweet in hashtag.tweets.all()]
        profile_tweet_dates = [tweet.save_date for profile in users_profiles for tweet in profile.tweets.all()]
        dates = set(hashtag_dates + profile_dates + hashtag_tweet_dates + profile_tweet_dates)
        dates = list(dates)

        trending_hashtags = self.api_pipeline.get_top_hashtags_worldwide()
        trending_hashtags.sort(key=lambda hashtag: hashtag.tweet_volume, reverse=True)
        trending_hashtags_chart = PlotPainter.plot_hashtags(trending_hashtags)

        if users_hashtags:
            current_hashtag = users_hashtags[0]

            hashtags_tweets = self.api_pipeline.get_recent_tweets_for_hashtag(current_hashtag.text, how_many=5)
            hashtags_tweets.sort(key=lambda tweet: tweet.retweets, reverse=True)
            hashtags_tweets_chart = PlotPainter.plot_tweets(hashtags_tweets)
        else:
            current_hashtag = None
            hashtags_tweets = None
            hashtags_tweets_chart = None

        if users_profiles:
            current_profile = users_profiles[0]

            profiles_tweets = self.api_pipeline.get_recent_tweets_for_author(current_profile.username, how_many=5)
            profiles_tweets.sort(key=lambda tweet: tweet.retweets, reverse=True)
            profiles_tweets_chart = PlotPainter.plot_tweets(hashtags_tweets)
        else:
            current_profile = None
            profiles_tweets = None
            profiles_tweets_chart = None

        return render(request, 'twitter_analyser/index.html', {'dates': dates,
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
        hashtag_input = request.POST.get('hashtag_input')
        if hashtag_input:
            hashtags_tweets = self.api_pipeline.get_recent_tweets_for_hashtag(request.POST.get('hashtag_input'))
            if hashtags_tweets:
                hashtag = Hashtag.objects.create(text=hashtag_input, save_date=datetime.datetime.now())
                for tweet in hashtags_tweets:
                    tweet.save()
                hashtag.tweets.add(*hashtags_tweets)
                request.user.appuser.followed_hashtags.add(hashtag)

        return redirect('twitter_analyser:index')
