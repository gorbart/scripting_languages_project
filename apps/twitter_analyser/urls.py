from django.conf.urls import url
from django.urls import path

from apps.twitter_analyser.views import IndexView, DateView, QueryView, QueryDateView, unfollow_hashtag, \
    unfollow_profile

app_name = 'twitter_analyser'

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    path(r'<str:query>/', QueryView.as_view(), name='query'),
    path(r'<int:year>/<int:month>/<int:day>/', DateView.as_view(), name='date'),
    path(r'<int:year>/<int:month>/<int:day>/<str:query>/', QueryDateView.as_view(), name='date_query'),
    path(r'unfollow/hashtag/<int:pk>/', unfollow_hashtag, name='unfollow_hashtag'),
    path(r'unfollow/profile/<int:pk>/', unfollow_profile, name='unfollow_profile'),
]
