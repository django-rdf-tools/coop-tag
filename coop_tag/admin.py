# -*- coding:utf-8 -*-

from django.contrib import admin
from coop_tag.settings import get_class
#from feincms.admin import tree_editor


class TaggedItemInline(admin.StackedInline):
    model = get_class('taggeditem')


# We just override the TreeEditor template to add some custom CSS
# and put the move cursor before the object title

# class TagTreeAdmin(tree_editor.TreeEditor):
#     def __init__(self, *args, **kwargs):
#         super(TagTreeAdmin, self).__init__(*args, **kwargs)
#         self.change_list_template = [
#             'admin/feincms/tag_tree_editor.html',
#             ]

#     def changelist_view(self, request, extra_context=None, *args, **kwargs):
#         if 'actions_column' not in self.list_display:
#             self.list_display.insert(0, 'actions_column')
#         return super(TagTreeAdmin, self).changelist_view(request, extra_context)


    # inlines = [
    #     TaggedItemInline
    # ]


admin.site.register(get_class('tag'))#, TagTreeAdmin)
