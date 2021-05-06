from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

from apps.twitter_analyser.utils.twitter_api_pipeline import TwitterApiPipeline
from apps.twitter_analyser.views.utils.get_utils import get_user_specifics, handle_trending_hashtags, \
    handle_current_hashtag, handle_current_profile
from apps.twitter_analyser.views.utils.post_utils import handle_new_following


class QueryView(LoginRequiredMixin, View):
    """
    QueryView class is used to handle rendering index page of Twitter Analyser with contents retrieved from Twitter API
    related to a query which can be followed hashtag's text or followed profile's username.
    Attributes:
        - api_pipeline TwitterApiPipeline object with credentials assigned to this project
    """

    api_pipeline = TwitterApiPipeline()

    def get(self, request, query):
        """
        get method renders index.html with contents retrieved from Twitter API related to followed Hashtag and
        TwitterProfile instances chosen by passing hashtag's text or profile's username (if there is hashtag text passed
        - Profile is the first one alphabetically and vice versa). It also saves the contents in database.
        :param query: hashtag text or profile's username
        :param request: GET request
        :return: rendered index.html page with dictionary containing current date (here None as we don't retrieve
        anything from database; only from Twitter API), list of dates application has been used, list of trending in the
        world hashtags retrieved from Twitter API, chart presenting their popularity, lists of hashtags and Twitter
        profiles followed by user, current hashtag (may be from query, otherwise alphabetically first), list of most
        popular posts related to it, chart presenting their statistics, current profile (may be from query, otherwise
        alphabetically first), list of most popular posts related to it and chart presenting their statistics
        """

        dates, trending_hashtags_from_db, users_hashtags, users_profiles = get_user_specifics(request)

        trending_hashtags, trending_hashtags_chart = handle_trending_hashtags(self.api_pipeline,
                                                                              trending_hashtags_from_db)

        if users_hashtags:
            current_hashtag = users_hashtags.filter(text=query)[0] if query[0] == '#' else users_hashtags[0]

            hashtags_tweets, hashtags_tweets_chart = handle_current_hashtag(self.api_pipeline, current_hashtag)
        else:
            current_hashtag = None
            hashtags_tweets = None
            hashtags_tweets_chart = None

        if users_profiles:
            current_profile = users_profiles.filter(username=query)[0] if query[0] != '#' else users_profiles[0]

            profiles_tweets, profiles_tweets_chart = handle_current_profile(self.api_pipeline, current_profile)
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

    def post(self, request, query):
        """
        post method is used to follow new hashtags and profiles
        :param query: query in view's url; ignored here
        :param request: POST request with demanded hashtag or profile username
        :return: redirection to index page
        """

        user_input = handle_new_following(request, self.api_pipeline)
        return redirect(f'/twitter_analyser/{user_input}')
