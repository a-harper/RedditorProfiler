from django.conf.urls import url

from . import views

urlpatterns = [
    # e.g. /redditor/
    url(r'^$', views.index, name='index'),
    # e.g. /redditor/filthyneckbeard/
    url(r'^(?P<username>[^/]+)$', views.redditor, name='redditor'),
    url(r'(?P<username>[^/]+)/r/(?P<subreddit>[^/]+)', views.subreddits, name='subreddits'),
]
