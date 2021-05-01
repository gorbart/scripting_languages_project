from django.conf.urls import url

from apps.twitter_analyser.views import IndexView

app_name = 'twitter_analyser'

urlpatterns = [
    url(r'^', IndexView.as_view(), name='index'),
]
