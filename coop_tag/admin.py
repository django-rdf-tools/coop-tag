# -*- coding:utf-8 -*-
from django.contrib import admin
from coop_tag.models import Ctag, TagCategory

admin.site.register(TagCategory)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category')
    list_editable = ('category',)
    search_fields = ['name', 'slug']
    list_filter = ('category',)

admin.site.register(Ctag, TagAdmin)
