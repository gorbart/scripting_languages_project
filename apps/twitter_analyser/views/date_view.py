import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from apps.twitter_analyser.models import Hashtag
from apps.twitter_analyser.utils.plot_painter import PlotPainter
from apps.twitter_analyser.utils.twitter_api_pipeline import TwitterApiPipeline
from apps.twitter_analyser.utils.utils import get_all_dates_for_user


class DateView(LoginRequiredMixin, View):
    api_pipeline = TwitterApiPipeline()

    def get(self, request, year, month, day):
        appuser = request.user.appuser
        users_hashtags = appuser.followed_hashtags.all()
        users_profiles = appuser.followed_profiles.all()

        trending_hashtags_from_db = Hashtag.objects.all()

        dates = get_all_dates_for_user(users_hashtags, users_profiles, trending_hashtags_from_db)

        current_date = datetime.datetime(year, month, day)

        trending_hashtags = Hashtag.objects.filter(appuser__isnull=True).filter(save_date=current_date).distinct()

        if trending_hashtags and trending_hashtags != set():
            trending_hashtags_list = [trending_hashtag for trending_hashtag in trending_hashtags]

            trending_hashtags_list.sort(key=lambda hashtag: hashtag.tweet_volume, reverse=True)
            trending_hashtags_chart = PlotPainter.plot_hashtags(trending_hashtags_list)
        else:
            trending_hashtags_list = None
            trending_hashtags_chart = None

        if users_hashtags:
            current_hashtag = users_hashtags[0]

            hashtags_tweets = current_hashtag.tweets.filter(save_date=current_date).distinct()

            hashtags_tweets_list = [hashtags_tweet for hashtags_tweet in hashtags_tweets]

            hashtags_tweets_list.sort(key=lambda tweet: tweet.retweets, reverse=True)
            hashtags_tweets_chart = PlotPainter.plot_tweets(hashtags_tweets_list)
        else:
            current_hashtag = None
            hashtags_tweets = None
            hashtags_tweets_chart = None

        if users_profiles:
            current_profile = users_profiles[0]

            profiles_tweets = current_profile.tweets.filter(save_date__eq=current_date).distinct()

            profiles_tweets_list = [profiles_tweet for profiles_tweet in profiles_tweets]

            profiles_tweets_list.sort(key=lambda tweet: tweet.retweets, reverse=True)
            profiles_tweets_chart = PlotPainter.plot_tweets(profiles_tweets_list)
        else:
            current_profile = None
            profiles_tweets_list = None
            profiles_tweets_chart = None

        return render(request, 'twitter_analyser/index.html', {'dates': dates,
                                                               'trending_hashtags': trending_hashtags_list,
                                                               'trending_hashtags_chart': trending_hashtags_chart,
                                                               'users_hashtags': users_hashtags,
                                                               'users_profiles': users_profiles,
                                                               'current_hashtag': current_hashtag,
                                                               'hashtags_tweets': hashtags_tweets,
                                                               'hashtags_tweets_chart': hashtags_tweets_chart,
                                                               'current_profile': current_profile,
                                                               'profiles_tweets': profiles_tweets_list,
                                                               'profiles_tweets_chart': profiles_tweets_chart})

    def post(self, request, year, month, day):
        hashtag_input = request.POST.get('hashtag_input')
        if hashtag_input:
            hashtags_tweets = self.api_pipeline.get_recent_tweets_for_hashtag(request.POST.get('hashtag_input'))
            if hashtags_tweets:
                hashtag = Hashtag.objects.create(text=hashtag_input, save_date=datetime.datetime.now())
                for tweet in hashtags_tweets:
                    tweet.save()
                hashtag.tweets.add(*hashtags_tweets)
                request.user.appuser.followed_hashtags.add(hashtag)

        return redirect('twitter_analyser:date', year, month, day)
