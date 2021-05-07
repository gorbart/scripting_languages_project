from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from apps.twitter_analyser.utils.email_report_sender import EmailReportSender
from apps.twitter_analyser.utils.twitter_api_pipeline import TwitterApiPipeline
from apps.twitter_analyser.views.utils.get_utils import get_user_specifics, handle_trending_hashtags, \
    handle_current_hashtag, handle_current_profile
from apps.twitter_analyser.views.utils.post_utils import handle_new_following


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

        dates, trending_hashtags_from_db, users_hashtags, users_profiles = get_user_specifics(request)

        trending_hashtags, trending_hashtags_chart = handle_trending_hashtags(self.api_pipeline,
                                                                              trending_hashtags_from_db)

        if users_hashtags:
            current_hashtag = users_hashtags[0]

            hashtags_tweets, hashtags_tweets_chart = handle_current_hashtag(self.api_pipeline, current_hashtag)
        else:
            current_hashtag = None
            hashtags_tweets = None
            hashtags_tweets_chart = None

        if users_profiles:
            current_profile = users_profiles[0]

            profiles_tweets, profiles_tweets_chart = handle_current_profile(self.api_pipeline, current_profile)
        else:
            current_profile = None
            profiles_tweets = None
            profiles_tweets_chart = None

        context = {'user': request.user,
                   'current_date': None,
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
                   'profiles_tweets_chart': profiles_tweets_chart}

        if request.GET.get('report_btn'):
            EmailReportSender.send_report(context)

        return render(request, 'twitter_analyser/index.html', context)

    def post(self, request):
        """
        post method is used to follow new hashtags and profiles
        :param request: POST request with demanded hashtag or profile username
        :return: redirection to index page
        """

        user_input = handle_new_following(request, self.api_pipeline)
        return redirect(f'/twitter_analyser/{user_input}')
