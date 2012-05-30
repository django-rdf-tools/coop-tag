# -*- coding:utf-8 -*-
from django.db import models
from taggit.models import TagBase, GenericTaggedItemBase
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django_extensions.db import fields as exfields
from positions.fields import PositionField
from coop.models import URIModel


# TODO http://redmine.django.coop/issues/117
# from django.template.defaultfilters import slugify as default_slugify
# import re
# from django.utils.safestring import mark_safe
# def unicode_slugify(value):
#     """
#     Normalizes string, converts to lowercase, removes non-alpha characters,
#     and converts spaces to hyphens.
#     """
#     value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
#     return mark_safe(re.sub('[-\s]+', '-', value))


class TagCategory(models.Model):
    label = models.CharField(_(u'label'), max_length=100)
    uri = models.CharField(_(u'tag URI'), blank=True, max_length=250, editable=False)
    slug = exfields.AutoSlugField(populate_from='label', blank=True)
    position = PositionField()

    def __unicode__(self):
        return self.label

    class Meta:
        verbose_name = _(u'tag category')
        verbose_name_plural = _(u'tag categories')
        ordering = ['position']
        
    
class Ctag(TagBase, URIModel):
    '''
    Defines a Common Tag resource
    '''
    # FIELDS name and slug are defined in TagBase   

    language = models.CharField(_(u'language'), max_length=10, default='fr')
    user = models.ForeignKey(User, blank=True, null=True, verbose_name=_(u'django user'), editable=False)
    person_uri = models.CharField(_(u'author URI'), blank=True, max_length=250, editable=False)
    created = exfields.CreationDateTimeField(_(u'created'))
    modified = exfields.ModificationDateTimeField(_(u'modified'))
    category = models.ForeignKey(TagCategory, null=True, blank=True, verbose_name=_(u'category'))
    # selectable = models.BooleanField(default=True)
    concept_uri = models.CharField(_(u'Concept URI'), blank=True, max_length=250, editable=False)

    def __init__(self, *args, **kwargs):
        super(Ctag, self).__init__(*args, **kwargs)
        slug = models.CharField(verbose_name=_('Slug'), unique=True, max_length=100)
        slug.contribute_to_class(self, 'slug')


    def get_absolute_url(self):
        return reverse('tag_detail', args=[self.slug])

    class Meta:
        verbose_name = _(u'tag')
        verbose_name_plural = _(u'tags') 

    # TODO http://redmine.django.coop/issues/117
    # def slugify(self, tag, i=None):
    #     slug = unicode_slugify(tag)
    #     if i is not None:
    #         slug += "_%d" % i
    #     return slug
           

class CtaggedItem(GenericTaggedItemBase):
    tag = models.ForeignKey(Ctag, related_name="ctagged_items")
    
    class Meta:
        verbose_name = _(u'tagged item')
        verbose_name_plural = _(u'tagged items')

