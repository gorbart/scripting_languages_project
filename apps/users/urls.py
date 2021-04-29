from django.conf.urls import url

from apps.users.views import RegisterView, LoginView, LogoutView

app_name = 'users'

urlpatterns = [
    url('register/', RegisterView.as_view(), name='register'),
    url('login/', LoginView.as_view(), name='login'),
    url('logout', LogoutView.as_view(), name='logout')
]
