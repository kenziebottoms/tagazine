from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    ### PROFILES
    # /profile/1
    url(r'^profile/(?P<profile_id>[0-9]+)/$', views.profiles.profile, name='profile'),
    # /profile/1/edit
    url(r'^profile/(?P<profile_id>[0-9]+)/edit/$', views.profiles.edit_profile, name='edit_profile'),

    ### ZINES
    # /zine/1
    url(r'^zine/(?P<zine_id>[0-9]+)/$', views.zines.zine, name='zine'),
    # /zine/new
    url(r'^zine/new/$', views.zines.new_zine, name='new_zine'),
    # /zine/white-fungus
    url(r'^zine/(?P<slug>[a-z0-9-]*)/$', views.zines.zine, name='zine'),
    # /zine/1/edit
    url(r'^zine/(?P<zine_id>[0-9]+)/edit/$', views.zines.edit_zine, name='edit_zine'),
    # /zine/white-fungus/edit
    url(r'^zine/(?P<slug>[a-z0-9-]*)/edit/$', views.zines.edit_zine, name='edit_zine'),

    ### ISSUES
    # /zine/1/issue/15
    url(r'^zine/(?P<zine_id>[0-9]+)/issue/(?P<issue_no>[0-9]+)/$', views.issues.issue, name='issue'),
    # /zine/1/issue/15/edit
    url(r'^zine/(?P<zine_id>[0-9]+)/issue/(?P<issue_no>[0-9]+)/edit/$', views.issues.edit_issue, name='edit_issue'),
    # /zine/1/issue/new
    url(r'^zine/(?P<zine_id>[0-9]+)/issue/new/$', views.issues.new_issue, name='new_issue'),

    ### ETC
    # /drafts
    url(r'^drafts/$', views.drafts, name='drafts'),
    # /dash
    url(r'^dash/$', views.dash, name='dash'),
    # /tag/anarchy
    url(r'^tag/(?P<slug>[a-z0-9-]*)$', views.tag, name='tag'),
    # /search/?term=feminism
    url(r'^search/$', views.search, name='search'),

    ### API ###
    # /api/get_tags/fe, /api/get_tags/fem, /api/get_tags/femi
    url(r'^api/get_tags/', views.api.get_tags, name='get_tags'),
    # /api/add_tag/
    url(r'^api/add_tag/', views.api.add_tag, name='add_tag'),
    # /api/reslug/zine/
    url(r'^api/reslug/zine/', views.api.zine_reslug, name='zine_reslug'),

    ### AUTH ###
    # /login
    url(r'^login/', views.auth.login_view, name='login_view'),
    # /logout
    url(r'^logout/', views.auth.logout_view, name='logout_view'),
    # /signup
    url(r'^signup/', views.auth.signup, name='signup'),
]