# -*- coding:utf-8 -*-

from django.contrib import admin
from coop_tag.settings import TAGGED_ITEM_MODEL, TAG_MODEL

# COOP
# admin.site.register(TagCategory)

print TAGGED_ITEM_MODEL, TAG_MODEL


class TaggedItemInline(admin.StackedInline):
    model = TAGGED_ITEM_MODEL


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')  # 'category')
    #list_editable = ('category',)
    search_fields = ['name', 'slug']
    #list_filter = ('category',)
    inlines = [
        TaggedItemInline
    ]

admin.site.register(TAG_MODEL, TagAdmin)

