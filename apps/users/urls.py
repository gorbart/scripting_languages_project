from django.conf.urls import url

from apps.users.views import RegisterView

app_name = 'users'

urlpatterns=[
    url(r'^register/$', RegisterView.as_view())
]