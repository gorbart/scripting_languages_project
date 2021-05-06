from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from apps.twitter_analyser.utils.twitter_api_pipeline import TwitterApiPipeline
from apps.twitter_analyser.views.utils.get_date_utils import get_user_specifics_for_date, \
    handle_trending_hashtags_for_date, handle_hashtags_tweets_for_date, handle_profiles_tweets_for_date
from apps.twitter_analyser.views.utils.post_utils import handle_new_following


class DateView(LoginRequiredMixin, View):
    """
    DateView class is used to handle rendering index page of Twitter Analyser with contents retrieved from database
    saved on a given date.
    Attributes:
        - api_pipeline TwitterApiPipeline object with credentials assigned to this project
    """

    api_pipeline = TwitterApiPipeline()

    def get(self, request, year, month, day):
        """
        get method renders index.html with contents retrieved from database related to the first alphabetically Hashtag
        and TwitterProfile instances and saved on given date.
        :param day: day of searched date
        :param month: month of searched date
        :param year: year of searched date
        :param request: GET request
        :return: rendered index.html page with dictionary containing current date (here year/month/date parameters),
        list of dates records have been saved in database, list of trending in the world hashtags on given day,
        chart presenting their popularity, lists of hashtags and Twitter profiles followed by user, current hashtag
        (alphabetically first), list of most popular posts related to it, chart presenting their
        statistics, current profile (alphabetically first), list of most popular posts
        related to it and chart presenting their statistics
        """

        current_date, dates, trending_hashtags, users_hashtags, users_profiles = get_user_specifics_for_date(day,
                                                                                                             month,
                                                                                                             year,
                                                                                                             request)

        trending_hashtags_chart, trending_hashtags_list = handle_trending_hashtags_for_date(trending_hashtags)

        if users_hashtags:
            current_hashtag = users_hashtags[0]

            hashtags_tweets_chart, hashtags_tweets_list = handle_hashtags_tweets_for_date(current_date,
                                                                                          current_hashtag)
        else:
            current_hashtag = None
            hashtags_tweets_list = None
            hashtags_tweets_chart = None

        if users_profiles:
            current_profile = users_profiles[0]

            profiles_tweets_chart, profiles_tweets_list = handle_profiles_tweets_for_date(current_date,
                                                                                          current_profile)
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

    def post(self, request, year, month, day):
        """
        post method is used to follow new hashtags and profiles
        :param day: day in view's url; ignored here
        :param month: month in view's url; ignored here
        :param year: year in view's url; ignored here
        :param request: POST request with demanded hashtag or profile username
        :return: redirection to index page
        """

        handle_new_following(request, self.api_pipeline)
        return redirect('twitter_analyser:index')
