from django.conf.urls import url
from django.urls import path

from apps.twitter_analyser.views import IndexView, DateView

app_name = 'twitter_analyser'

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    path(r'<int:year>/<int:month>/<int:day>/', DateView.as_view(), name='date'),
]
