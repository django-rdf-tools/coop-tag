# -*- coding:utf-8 -*-
from django.contrib import admin
from coop_tag.models import Ctag,TagCategory

admin.site.register(TagCategory)


class TagAdmin(admin.ModelAdmin):
    search_fields = ['name','slug']
    list_filter = ('category',)

admin.site.register(Ctag,TagAdmin)
