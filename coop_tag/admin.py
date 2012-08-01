# -*- coding:utf-8 -*-

from django.contrib import admin
from coop_tag.settings import get_class
from feincms.admin import tree_editor


class TaggedItemInline(admin.StackedInline):
    model = get_class('taggeditem')


class TagAdmin(tree_editor.TreeEditor):
    inlines = [
        TaggedItemInline
    ]

admin.site.register(get_class('tag'), TagAdmin)
