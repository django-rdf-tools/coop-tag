# -*- coding:utf-8 -*-


import copy
from django import forms
from coop_tag import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from coop_tag.utils import edit_string_for_tags

from django.forms.widgets import CheckboxSelectMultiple, CheckboxInput
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape


class GroupedCheckboxSelectMultiple(CheckboxSelectMultiple):
    class Media:
        js = ('%sjs/autocolumn.js' % settings.TAGGER_STATIC_URL,
              '%sjs/groupbox.js' % settings.TAGGER_STATIC_URL)

    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = []
        has_id = attrs and 'id' in attrs
        final_attrs = self.build_attrs(attrs, name=name)
        # Normalize to strings
        str_values = set([force_unicode(v) for v in value])
        output = [u'<div class="groupbox">']
        for z, g in enumerate(self.choices):
            output.append(u'<div class="groupbox-header">%s <span class="group-count">(<span></span>)</span></div>' % g[0])
            output.append(u'<ul class="groupbox-list">')
            for i, (option_value, option_label) in enumerate(g[1]):
                # If an ID attribute was given, add a numeric index as a suffix,
                # so that the checkboxes don't all have the same ID attribute.
                if has_id:
                    final_attrs = dict(final_attrs, id='%s_%s_%s' % (attrs['id'], z, i))
                    label_for = u' for="%s"' % final_attrs['id']
                else:
                    label_for = ''

                cb = CheckboxInput(final_attrs, check_test=lambda value: value in str_values)
                option_value = force_unicode(option_value)
                rendered_cb = cb.render(name, option_value)
                option_label = conditional_escape(force_unicode(option_label))
                output.append(u'<li><label%s>%s %s</label></li>' % (label_for, rendered_cb, option_label))
            output.append(u'</ul>')
        output.append(u'</div>')
        return mark_safe(u'\n'.join(output))

    def id_for_label(self, id_):
        # See the comment for RadioSelect.id_for_label()
        if id_:
            id_ += '_0'
        return id_
    id_for_label = classmethod(id_for_label)


class TagAutoSuggest(forms.TextInput):
    input_type = 'text'

    def render(self, name, value, attrs=None):
        if value is not None and not isinstance(value, basestring):
            tags = [o.tag for o in value.select_related("tag")]
            value = edit_string_for_tags(tags)

        result_attrs = copy.copy(attrs)
        result_attrs['type'] = 'hidden'
        result_html = super(TagAutoSuggest, self).render(name, value,
            result_attrs)

        widget_attrs = copy.copy(attrs)
        widget_attrs['id'] += '__tagautosuggest'
        widget_html = super(TagAutoSuggest, self).render(name, value,
            widget_attrs)

        js = u"""
            <script type="text/javascript">
            (function ($) {
                var tags_as_string;

                $(document).ready(function (){
                    tags_as_string = $('#%(result_id)s').val();

                    $("#%(widget_id)s").autoSuggest("%(url)s", {
                        asHtmlID: "%(widget_id)s",
                        startText: "%(start_text)s",
                        emptyText: "%(empty_text)s",
                        limitText: "%(limit_text)s",
                        preFill: tags_as_string,
                        queryParam: 'q',
                        retrieveLimit: %(retrieve_limit)d,
                        minChars: 1,
                        neverSubmit: true
                    });

                    $('.as-selections').addClass('vTextField');
                    $('ul.as-selections li.as-original input').addClass('vTextField');

                    $('#%(result_id)s').parents().find('form').submit(function (){
                        tags_as_string = $("#as-values-%(widget_id)s").val();
                        $("#%(widget_id)s").remove();
                        $("#%(result_id)s").val(tags_as_string);
                    });
                });
            })(django.jQuery);
            </script>""" % {
                'result_id': result_attrs['id'],
                'widget_id': widget_attrs['id'],
                'url': reverse('tag-autosuggest-list'),
                'start_text': _("Enter Tag Here"),
                'empty_text': _("No Results"),
                'limit_text': _('No More Selections Are Allowed'),
                'retrieve_limit': settings.TAGGER_MAX_SUGGESTIONS,
            }
        return result_html + widget_html + mark_safe(js)

    class Media:
        css = {
            'all': ('%s/css/%s' % (settings.TAGGER_STATIC_URL, settings.TAGGER_CSS_FILENAME),)
        }
        js = (
            '%s/js/jquery.autoSuggest.minified.js' % settings.TAGGER_STATIC_URL,
        )
