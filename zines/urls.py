from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # /profile/1
    url(r'^profile/(?P<profile_id>[0-9]+)/$', views.profile, name='profile'),
    # /profile/1/edit
    url(r'^profile/(?P<profile_id>[0-9]+)/edit/$', views.edit_profile, name='edit_profile'),
    # /zine/1
    url(r'^zine/(?P<zine_id>[0-9]+)/$', views.zine, name='zine'),
    # /zine/1/edit
    url(r'^zine/(?P<zine_id>[0-9]+)/edit/$', views.edit_zine, name='edit_zine'),
    # /zine/1/issue/15
    url(r'^zine/(?P<zine_id>[0-9]+)/issue/(?P<issue_no>[0-9]+)/$', views.issue, name='issue'),
]