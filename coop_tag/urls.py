#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('coop_tag.views',
    url(r'^tag/(?P<slug>[\w-]+)/$', 'tag_detail', name="tag_detail"),
    url(r'^list/$', 'list_tags', name='tag-autosuggest-list'),
)

