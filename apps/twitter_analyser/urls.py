from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.twitter_analyser.views import IndexView

app_name = 'twitter_analyser'

urlpatterns = [
    url(r'^', login_required(IndexView.as_view()), name='index'),
]
