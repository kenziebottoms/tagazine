from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # /user/1
    url(r'^user/(?P<user_id>[0-9]+)/$', views.user, name='user'),
    # /zine/1
    url(r'^zine/(?P<zine_id>[0-9]+)/$', views.zine, name='zine'),
    # /zine/1/issue/15
    url(r'^zine/(?P<zine_id>[0-9]+)/issue/(?P<issue_no>[0-9]+)/$', views.issue, name='issue'),
]