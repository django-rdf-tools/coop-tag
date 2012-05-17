from django.forms.widgets import CheckboxSelectMultiple, CheckboxInput
from django.utils.encoding import force_unicode
from itertools import chain
from django.utils.safestring import mark_safe
from django.utils.html import conditional_escape


class GroupedCheckboxSelectMultiple(CheckboxSelectMultiple):
    class Media:
        js = ('js/autocolumn.js',
              'js/groupbox.js')
    
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

    