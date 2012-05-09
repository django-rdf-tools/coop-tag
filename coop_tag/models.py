# -*- coding:utf-8 -*-
from django.db import models
from taggit.models import TagBase, GenericTaggedItemBase
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django_extensions.db import fields as exfields
from positions.fields import PositionField


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
        
    
class Ctag(TagBase):
    '''
    Defines a Common Tag resource
    '''
    # FIELDS name and slug are defined in TagBase    
    language = models.CharField(_(u'language'), max_length=10, default='fr')
    user = models.ForeignKey(User, blank=True, null=True, verbose_name=_(u'django user'), editable=False)
    uri = models.CharField(_(u'tag URI'), blank=True, max_length=250, editable=False)
    author_uri = models.CharField(_(u'author URI'), blank=True, max_length=250, editable=False)
    created = exfields.CreationDateTimeField(_(u'created'))
    modified = exfields.ModificationDateTimeField(_(u'modified'))
    category = models.ForeignKey(TagCategory, null=True, blank=True, verbose_name=_(u'category'))
    # selectable = models.BooleanField(default=True)
    concept_uri = models.CharField(_(u'Concept URI'), blank=True, max_length=250, editable=False)

    def get_absolute_url(self):
        return reverse('tag_detail', args=[self.slug])

    class Meta:
        verbose_name = _(u'tag')
        verbose_name_plural = _(u'tags') 
           

class CtaggedItem(GenericTaggedItemBase):
    tag = models.ForeignKey(Ctag, related_name="ctagged_items")
    
    class Meta:
        verbose_name = _(u'tagged item')
        verbose_name_plural = _(u'tagged items')

