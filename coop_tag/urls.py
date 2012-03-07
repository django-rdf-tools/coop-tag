#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^tag/(?P<slug>[\w-]+)/$', 'coop_tag.views.tag_detail', name="tag_detail"),
)
